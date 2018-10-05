I would attempt the problem to understand the probabilites of transition from one state to another state. 

States in this problem are the Pagenames. eg : Home, Search, Checkout and Buy.



Lets call the original, data set as OriginalTable

SQL code

steps:

rank the time for each sessionID
create states
calculate probabilities for transitions
pick the max conditional prob
------------------------------------------------------------------------------------------------------------------------------------------------

With Temptable_1 as

(

Select Time, SessionID, PageName, rank() over(partition by SessionID order by Time) as TimeRank from OriginalTable

),

with Temptable_2 as

(

select SessionID, A.PageName as state_1, B.PageName as state_2, C.PageName as state_3

from Temptable_1 A join Temptable_1 B on A.SessionID = B.SessionID and A.TimeRank+1 = B.TimeRank

join Temptable_1 C on B.SessionID = C.SessionID and B.TimeRank+1 = C.TimeRank



),

with Temptable_3 as

(

select state_1, count(*) as state_1_count from Temptable_2 group by state_1

),

with Temptable_4 as

(select state_1, state_2, count(*) as state_1_2_count from Temptable_2 group by state_1, state_2),

with Temptable_5 as

(

select state_1, state_2, state_3, count(*) as state_1_2_3_count from Temptable_2 group by state_1, state_2, state_3

)

select A.state_1, A.state_2, A.state_3,

A.state_1_2_3_count/B.state_1_2_count as trans_2_3_prob,

B.state_1_2_count/C.state_1_count as trans_1_2_prob

from Temptable_5 A join Temptable_4 B on A.state_1 = B.state_1 and A.state_2 = B.state_2

join Temptable_3 C on B.state_1 = C.state_1

------------------------------------------------------------------------------------------------------------------------------------------------

Now, we have the transition probabilities between states considering all trigrams of the data.

To find the best possible state_3, for a given state_1 and state_2, we will directly go to the SQL final output to fetch the record with highest trans_2_3_prob value.

This implementation is nothing but Markov Chains - Trigram model.