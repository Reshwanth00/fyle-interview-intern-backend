-- Find the number of grade A's given by the teacher who has graded the most assignments
WITH TeacherGradingCount AS (
    SELECT
        teacher_id,
        COUNT(*) AS total_assignments_graded
    FROM
        assignments
    WHERE
        state = 'GRADED'
    GROUP BY
        teacher_id
    ORDER BY
        total_assignments_graded DESC
    LIMIT 1
)
SELECT
    COUNT(*) AS grade_a_count
FROM
    assignments
WHERE
    grade = 'A'
    AND teacher_id = (SELECT teacher_id FROM TeacherGradingCount);
