from collections import defaultdict
from decimal import Decimal
from .models import StudentResult


def get_available_classes(academic_year=None):
    """Returns a sorted list of distinct class labels like ['9A', '9B', '10A', '11A', '12B']."""
    qs = StudentResult.objects.select_related('student', 'subject_ref').all()
    if academic_year:
        qs = qs.filter(academic_year=academic_year)

    labels = {res.class_label for res in qs if res.class_label and res.class_label != "Unassigned"}

    def _sort_key(label):
        digits = ''.join(ch for ch in label if ch.isdigit())
        letters = ''.join(ch for ch in label if ch.isalpha())
        return (int(digits) if digits else 999, letters)

    return sorted(labels, key=_sort_key)


def compute_class_standings(class_label, academic_year=None):
    """
    Computes Semester 1, Semester 2, and Combined Annual totals, averages, and ranks
    for every student in `class_label` (e.g., '9A', '10B', '11A', '12B'), plus
    per-subject class averages for Semester 1 & Semester 2.
    """
    target_class = (class_label or "").strip().upper()
    qs = StudentResult.objects.select_related('student', 'subject_ref').all()
    if academic_year:
        qs = qs.filter(academic_year=academic_year)

    class_results = [r for r in qs if r.class_label.upper() == target_class]

    # Group results by RegisteredStudent
    by_student = defaultdict(list)
    for res in class_results:
        by_student[res.student].append(res)

    # Track per-subject scores across the class for Semester 1 & 2
    subject_scores_sem1 = defaultdict(list)
    subject_scores_sem2 = defaultdict(list)

    student_rows = []
    for reg_student, res_list in by_student.items():
        sem1_results = sorted(
            [r for r in res_list if r.semester == 1],
            key=lambda r: (r.subject_ref.name if r.subject_ref else r.subject).lower()
        )
        sem2_results = sorted(
            [r for r in res_list if r.semester == 2],
            key=lambda r: (r.subject_ref.name if r.subject_ref else r.subject).lower()
        )

        for r in sem1_results:
            subj_name = r.subject_ref.name if r.subject_ref else r.subject
            subject_scores_sem1[subj_name].append(r.score)

        for r in sem2_results:
            subj_name = r.subject_ref.name if r.subject_ref else r.subject
            subject_scores_sem2[subj_name].append(r.score)

        sem1_total = sum((r.score for r in sem1_results), Decimal('0.00'))
        sem2_total = sum((r.score for r in sem2_results), Decimal('0.00'))

        sem1_avg = round(sem1_total / len(sem1_results), 2) if sem1_results else None
        sem2_avg = round(sem2_total / len(sem2_results), 2) if sem2_results else None

        if sem1_avg is not None and sem2_avg is not None:
            overall_avg = round((sem1_avg + sem2_avg) / Decimal('2'), 2)
        elif sem1_avg is not None:
            overall_avg = sem1_avg
        elif sem2_avg is not None:
            overall_avg = sem2_avg
        else:
            overall_avg = None

        student_rows.append({
            'student': reg_student,
            'full_name': f"{reg_student.first_name} {reg_student.last_name}".strip(),
            'student_id': reg_student.student_id,
            'sem1_results': sem1_results,
            'sem2_results': sem2_results,
            'sem1_total': sem1_total,
            'sem2_total': sem2_total,
            'sem1_avg': sem1_avg,
            'sem2_avg': sem2_avg,
            'overall_avg': overall_avg,
            'sem1_rank': None,
            'sem2_rank': None,
            'overall_rank': None,
        })

    # Standard competition ranking (1, 2, 2, 4 for ties)
    def _assign_ranks(rows, avg_key, rank_key):
        ranked = [r for r in rows if r[avg_key] is not None]
        ranked.sort(key=lambda r: r[avg_key], reverse=True)
        last_score = None
        last_rank = 0
        for idx, row in enumerate(ranked, start=1):
            if row[avg_key] != last_score:
                last_rank = idx
                last_score = row[avg_key]
            row[rank_key] = last_rank

    _assign_ranks(student_rows, 'sem1_avg', 'sem1_rank')
    _assign_ranks(student_rows, 'sem2_avg', 'sem2_rank')
    _assign_ranks(student_rows, 'overall_avg', 'overall_rank')

    student_rows.sort(
        key=lambda r: (r['overall_rank'] is None, r['overall_rank'] or 9999, r['full_name'])
    )

    # Combine per-subject averages across Semester 1 & Semester 2
    all_subjects = sorted(set(subject_scores_sem1.keys()) | set(subject_scores_sem2.keys()))
    subject_averages = []
    subject_avg_map = {}

    for subj in all_subjects:
        s1_list = subject_scores_sem1.get(subj, [])
        s2_list = subject_scores_sem2.get(subj, [])
        s1_avg = round(sum(s1_list, Decimal('0.00')) / len(s1_list), 2) if s1_list else None
        s2_avg = round(sum(s2_list, Decimal('0.00')) / len(s2_list), 2) if s2_list else None

        if s1_avg is not None and s2_avg is not None:
            combined_avg = round((s1_avg + s2_avg) / Decimal('2'), 2)
        else:
            combined_avg = s1_avg if s1_avg is not None else s2_avg

        entry = {
            'subject': subj,
            'sem1_avg': s1_avg,
            'sem2_avg': s2_avg,
            'combined_avg': combined_avg,
        }
        subject_averages.append(entry)
        subject_avg_map[subj] = entry

    return {
        'class_label': target_class,
        'total_in_class': len(student_rows),
        'students': student_rows,
        'subject_averages': subject_averages,
        'subject_avg_map': subject_avg_map,
    }