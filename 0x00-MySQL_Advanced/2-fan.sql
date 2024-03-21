-- ranks country origins of bands, ordered by the number of (non-unique) fans
-- Requirements:
-- 	Import this table dump: metal_bands.sql.zip
--	Column names must be: origin and nb_fans
--	Your script can be executed on any database

select origin,
       sum(fans) as nb_fans
from metal_bands
group by origin
order by nb_fans desc;
