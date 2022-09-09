select name, diff, release 
from(
    select *, release - lag(release) over(partition by idproducer order by release) diff 
        from(
            select * 
            from (
                    select a.name,a.id as idproducer, b.idmovie from producer a left join movieproducer b on a.id = b.idproducer
            ) 
            as movie_producer inner join movie a on a.id=movie_producer.idmovie where a.winner=true 
        )as data_table 
    ) where diff is not null