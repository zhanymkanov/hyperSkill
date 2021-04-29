-- Get unique users by dates and action_id
SELECT toDate(time) as date, action_id, count(distinct user_id) as num_users
FROM analytics.facts_events
GROUP BY date, action_id
ORDER BY date, action_id;