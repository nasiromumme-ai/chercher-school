document.addEventListener("DOMContentLoaded", function () {
    const gradeField = document.getElementById("id_grade");
    const streamField = document.getElementById("id_stream");
    const subjectsSelect = document.getElementById("id_subjects");

    if (!gradeField || !streamField || !subjectsSelect) {
        return;
    }

    function syncSubjectsWithFilterBox(selectedIdsSet) {
        // Standard <select multiple>
        Array.from(subjectsSelect.options).forEach((opt) => {
            opt.selected = selectedIdsSet.has(String(opt.value));
        });

        // Django admin filter_horizontal uses #id_subjects_from and #id_subjects_to
        const fromBox = document.getElementById("id_subjects_from");
        const toBox = document.getElementById("id_subjects_to");

        if (fromBox && toBox) {
            const allOptions = [
                ...Array.from(toBox.options),
                ...Array.from(fromBox.options),
            ];

            // Clear both boxes and redistribute cleanly
            toBox.innerHTML = "";
            fromBox.innerHTML = "";

            allOptions.forEach((opt) => {
                opt.selected = false;
                if (selectedIdsSet.has(String(opt.value))) {
                    toBox.appendChild(opt);
                } else {
                    fromBox.appendChild(opt);
                }
            });

            // Keep underlying <select id="id_subjects"> in sync
            Array.from(subjectsSelect.options).forEach((opt) => {
                opt.selected = selectedIdsSet.has(String(opt.value));
            });
        }

        subjectsSelect.dispatchEvent(new Event("change", { bubbles: true }));
    }

    async function updateSubjectsForSelection() {
        const grade = gradeField.value;
        const stream = streamField.value;

        const url = `/academics/admin/subjects-for-grade-stream/?grade=${encodeURIComponent(grade)}&stream=${encodeURIComponent(stream)}`;
        try {
            const response = await fetch(url, { credentials: "same-origin" });
            if (!response.ok) return;
            const data = await response.json();
            const idSet = new Set((data.subject_ids || []).map(String));
            syncSubjectsWithFilterBox(idSet);
        } catch (err) {
            console.error("Failed to load subjects for grade/stream:", err);
        }
    }

    gradeField.addEventListener("change", updateSubjectsForSelection);
    streamField.addEventListener("change", updateSubjectsForSelection);
});