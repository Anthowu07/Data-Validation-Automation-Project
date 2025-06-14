-- Null emails
SELECT user_id
FROM users
WHERE email IS NULL;
-- Invalid statuses
SELECT txn_id,
    status
FROM transactions
WHERE status NOT IN ('success', 'failed', 'pending');
-- Unknown links
SELECT t.txn_id
FROM transactions t
    LEFT JOIN users u ON t.user_id = u.user_id
WHERE u.user_is IS NULL;