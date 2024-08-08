WITH TeacherGradingCount AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_graded
    FROM
        assignments
    GROUP BY
        teacher_id
),
MaxGradedTeacher AS (
    SELECT
        teacher_id
    FROM
        TeacherGradingCount
    WHERE
        total_graded = (SELECT MAX(total_graded) FROM TeacherGradingCount)
)
SELECT
    COUNT(*) AS grade_A_count
FROM
    assignments
WHERE
    teacher_id IN (SELECT teacher_id FROM MaxGradedTeacher)
    AND grade = 'A'
