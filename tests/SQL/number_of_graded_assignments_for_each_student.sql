-- Get the number of graded assignments for each student
SELECT
    student_id,
    COUNT(*) AS graded_assignments_count
FROM
    assignments
WHERE
    state = 'GRADED'
GROUP BY
    student_id;
