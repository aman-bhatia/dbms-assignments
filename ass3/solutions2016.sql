--1--

with t1 as (select did,count(*) from movieDirectors group by did) select round(cast((select sum(count) from t1)::float/(select count(*) from t1)::float as numeric),6) as avg;

--2--

select count(*) from userProfile where country like 'India';

--3--

select ROUND(avg(age), 3) FROM userProfile;

--4--
select fname, lname from actor where id in (select pid from casts where mid in (select id from movie where name='Officer 444')) order by fname;

--5--

select distinct fname, lname from directors d, movieDirectors md, movie m, genre g where ((mod(cast(extract(year from m.year) as int), 4) = 0 and mod(cast(extract(year from m.year) as int), 100) <> 0) or mod(cast(extract(year from m.year) as int), 400) = 0) and m.id = md.mid and d.id = md.did and m.id = g.mid and g.genre = 'Film-Noir' order by fname; 



--6--
select fname, lname from actor where id in (select distinct pid from casts where mid in (select id from movie where cast(extract(year from year) as int)>=1990 and cast(extract(year from year) as int)<=2000)) order by fname;


--7--

select count(*) from userProfile where userid not in (select distinct userid from ratings);

--8--

select count(*) from userProfile where registered > '2006-01-01';


--9--

with t as (select did, count(*) as c from movieDirectors group by did having count(*)>=500 order by c desc) select fname, c from directors, t where directors.id=t.did order by c desc;


--10--

with t as (select mid, count(*) as c from casts group by mid order by c desc) select name, c from movie,t where movie.id=t.mid order by c desc,name;

--11--

with t as (with ca as (select * from actor, casts where actor.id=casts.pid) select did, count(case gender when 'F' then 1 else null end) as F, count(case gender when 'M' then 1 else null end) as M from movieDirectors, ca where ca.mid=movieDirectors.mid group by did) select fname, cast(t.F*1.0/t.M as decimal(10,6)) as rat from t,directors where t.M!=0 and t.did=id order by fname;


--12--
with t as(with l as(select actor.fname as col1, actor.lname as col11, genre.genre as col2, count(*) as count from genre, movie, casts, actor where genre.mid = movie.id and movie.id = casts.mid and casts.pid = actor.id group by actor.fname,actor.lname,genre.genre) select col1, max(count) as c from l group by col1), l as (select actor.fname as col1, actor.lname as col11, genre.genre as col2, count(*) as count from genre, movie, casts, actor where genre.mid = movie.id and movie.id = casts.mid and casts.pid = actor.id group by actor.fname,actor.lname,genre.genre) select t.col1, l.col2 from t, l where l.count = t.c and l.col1 = t.col1 order by t.col1 asc;


--13--
with q as (with t as (with ca as (select * from actor, casts where actor.id=casts.pid) select movie.id, movie.name, count(case gender when 'F' then 1 else null end) as F, count(case gender when 'M' then 1 else null end) as M from movie, ca where ca.mid=movie.id group by movie.id, name) select t.name, cast(t.F*1.0/t.M as decimal(10,6)) as rat from t where t.M!=0) select q.name from q order by q.rat;


--14--

Select p.name from (select m2.name from (select distinct r.mid, r.rating from ratings r where r.mid in (select id from movie where extract(year from year)>1990 and extract(year from year)<2000)) as m, movie m2 where m.mid=m2.id order by m.rating desc limit 10) as p order by p.name;


--15--

with t2 as (with t as(select ratings.userid, max(rating) as mr from ratings,userprofile where age>=13 and age<=21 and ratings.userid=userprofile.userid group by ratings.userid) select t.userid, mid from ratings,t where t.mr = ratings.rating and t.userid = ratings.userid) select distinct movie.name from t2, movie where t2.mid=movie.id order by movie.name;

--16--

select country from ratings,userprofile where ratings.userid=userprofile.userid group by country order by count(*) desc limit 5;

--17--

select cast(count(case gender when 'f' then 1 else null end)*1.0/count(case gender when 'm' then 1 else null end)*1.0 as decimal(10,6)) from userProfile right join ratings on userProfile.userid=ratings.userid;


--18--
with u as (with s as (with t as (select userid,did,max(rating) as c from ratings, movieDirectors where ratings.mid=movieDirectors.mid group by userid, did) select userid, directors.fname, directors.lname, t.c from t,directors where t.did=directors.id) select s.userid, max(s.c) as m from s group by s.userid), s2 as ( with t as (select userid,did,max(rating) as c from ratings, movieDirectors where ratings.mid=movieDirectors.mid group by userid, did) select userid, directors.fname, directors.lname, t.c from t,directors where t.did=directors.id) select u.userid,s2.fname,s2.lname from u,s2 where u.userid=s2.userid and u.m=s2.c;

--19--
with u as (with s as (with t as (select userid,did,avg(rating) as c from ratings, movieDirectors where ratings.mid=movieDirectors.mid group by userid, did) select userid, directors.fname, directors.lname, t.c from t,directors where t.did=directors.id) select s.userid, max(s.c) as m from s group by s.userid), s2 as ( with t as (select userid,did,avg(rating) as c from ratings, movieDirectors where ratings.mid=movieDirectors.mid group by userid, did) select userid, directors.fname, directors.lname, t.c from t,directors where t.did=directors.id) select u.userid,s2.fname,s2.lname from u,s2 where u.userid=s2.userid and u.m=s2.c;


--20--
with t1 as (select genre, avg(rating) as average, count(rating) as rated from ratings, genre where ratings.mid=genre.mid group by genre), t2 as (select genre, count(id) as total from movie,genre where movie.id=genre.mid group by genre) select t1.genre, cast(t1.average as decimal(10,6)), t1.rated, cast(t1.rated*100.0/t2.total as decimal(10,6)) as rated_percentage from t1,t2 where t1.genre=t2.genre order by t1.average;

--21--
with t1 as (with inratings as (select * from ratings,userprofile where ratings.userid=userprofile.userid and country='India' )select pid, avg(rating) as rating, count(*) as c from inratings,casts where inratings.mid=casts.mid group by pid having count(*)>=5) select fname,lname, rating from t1,actor where t1.pid=actor.id order by rating desc;

--22--
with l as (with t as(select userid, max(rating) as mr from ratings group by userid) select t.userid, mid from ratings,t where t.mr = ratings.rating and t.userid = ratings.userid) select distinct l.userid from l where l.mid in (with t2 as (with t as(select userid, max(rating) as mr from ratings group by userid) select t.userid, mid from ratings,t where t.mr = ratings.rating and t.userid = ratings.userid) select mid from t2 where t2.userid = 'user_000085') order by l.userid;

--23--
with movie2 as (select id, extract(year from year) as year from movie) select year, avg(rating) from movie2, ratings where movie2.id=ratings.mid group by year order by avg(rating);


--24--
with t2 as (select did,count(*) as c from movieDirectors where mid in (select distinct mid from casts where role='Himself' or role='Themselves') group by did order by c desc limit 1) select fname, c from directors, t2 where directors.id=t2.did;


--25--
select userid from ratings group by userid order by count(*) desc limit 10;

--29--
with t3 as (with t2 as (select mid,extract(year from year) as year, pid from casts,movie where casts.mid=movie.id) select year, avg(rating) from ratings,t2 where t2.mid=ratings.mid and pid in ((with t1 as (select pid,mid,count(*) from casts group by pid,mid) select pid from t1 group by pid order by count(*) desc limit 1)) group by year) select year, avg from t3 where year>=1990 and year<=1995 order by year;

--30--

with t as(with l as(select directors.fname as col1, directors.lname as col11, actor.fname as a1, actor.lname as a2, count(*) as count from directors, movieDirectors, casts, actor where directors.id = movieDirectors.did and movieDirectors.mid = casts.mid and casts.pid = actor.id group by directors.fname, directors.lname, actor.fname,actor.lname) select col1, max(count) as c from l group by col1), l as (select directors.fname as col1, directors.lname as col11, actor.fname as a1, actor.lname as a2, count(*) as count from directors, movieDirectors, casts, actor where directors.id = movieDirectors.did and movieDirectors.mid = casts.mid and casts.pid = actor.id group by directors.fname, directors.lname, actor.fname,actor.lname) select t.col1, l.a1 from t, l where l.count = t.c and l.col1 = t.col1 order by t.col1 asc;

