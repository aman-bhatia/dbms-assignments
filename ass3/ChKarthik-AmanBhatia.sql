--1--

SELECT ROUND(CAST((SELECT CAST(COUNT(*) as float) FROM movie)/(SELECT COUNT(*) FROM directors) as numeric), 6) AS AvgMoviesDirector;

--2--

SELECT COUNT(*) AS UserFromIndia FROM (SELECT DISTINCT ind.userid FROM ratings INNER JOIN (SELECT userProfile.userid FROM userProfile WHERE country='India')ind ON ratings.userid=ind.userid) ratind;

--3--

SELECT ROUND(avg(age), 3) AS AvgAgeUsers FROM userProfile, ratings WHERE userProfile.userid=ratings.userid;

--4--

SELECT DISTINCT actor.fname, actor.lname FROM actor INNER JOIN (SELECT casts.pid, casts.mid FROM casts INNER JOIN (SELECT id FROM movie WHERE name='Officer 444') mov ON casts.mid=mov.id) cas ON actor.id=cas.pid ORDER BY actor.fname;

--5--

SELECT DISTINCT movdir.fname, movdir.lname FROM (SELECT * FROM directors INNER JOIN movieDirectors ON directors.id=movieDirectors.did) movdir INNER JOIN (SELECT * FROM (SELECT * FROM movie WHERE ((cast(EXTRACT(YEAR FROM movie.year) as int) % 4 = 0) AND ((cast(EXTRACT(YEAR FROM movie.year) as int) % 100 <> 0) OR (cast(EXTRACT(YEAR FROM movie.year) as int) % 400 = 0)))) leapmov INNER JOIN (Select * FROM genre WHERE genre.genre='Film-Noir') gen ON leapmov.id=gen.mid) mov ON movdir.mid=mov.id ORDER BY movdir.fname;

--6--

SELECT DISTINCT actor.fname, actor.lname FROM actor INNER JOIN (SELECT * FROM casts INNER JOIN (SELECT * FROM movie WHERE ((cast(EXTRACT(YEAR FROM movie.year) as int)<=2000) AND (cast(EXTRACT(YEAR FROM movie.year) as int)>=1990))) yearmov ON casts.mid=yearmov.id) castyear ON actor.id=castyear.pid ORDER BY actor.fname;

--7--

SELECT COUNT(*) FROM (Select userProfile.userid FROM userProfile except (SELECT userProfile.userid FROM userProfile INNER JOIN ratings ON userProfile.userid=ratings.userid))rated;

--8--

SELECT COUNT(*) FROM userProfile WHERE userProfile.registered>='2006-01-01';

--9--

SELECT directors.fname, freq.Frequency FROM (SELECT did, COUNT(did) AS Frequency FROM movieDirectors GROUP BY did HAVING COUNT(did)>=500) freq INNER JOIN directors ON freq.did=directors.id ORDER BY frequency DESC;

--10--

SELECT movie.name, freqM.NofA FROM movie, (SELECT mid, COUNT(pid) AS NofA FROM casts GROUP BY mid) freqM WHERE movie.id=freqM.mid ORDER BY freqM.NofA DESC, movie.name;

--11--

SELECT directors.fname, ROUND(CAST(D.ratio as numeric), 6) as FbyMratio FROM (SELECT movieDirectors.did, CAST(SUM(F.fcount) as float)/SUM(M.mcount) as ratio FROM movieDirectors, (SELECT casts.mid, COUNT(actor.id) as fcount FROM casts, actor WHERE casts.pid=actor.id AND actor.gender='F' GROUP BY casts.mid) F, (SELECT casts.mid, COUNT(actor.id) as mcount FROM casts, actor WHERE casts.pid=actor.id AND actor.gender='M' GROUP BY casts.mid) M WHERE movieDirectors.mid=F.mid AND movieDirectors.mid=M.mid GROUP BY movieDirectors.did) D, directors WHERE D.did=directors.id ORDER BY directors.fname;

--12--

select actor_name, gen from (select actor.fname as actor_name,genre.genre as gen,count((actor.id,genre.genre)),rank() over (partition by actor.id order by count((actor.id,genre.genre)) desc) as rank from actor,casts,genre where actor.id=casts.pid and casts.mid=genre.mid group by actor.id, actor.fname,genre.genre) as foo where rank=1 order by actor_name;

--13--

SELECT F.name FROM (SELECT movie.name, CAST(F.fcount as float)/M.mcount AS ratio FROM movie, (SELECT casts.mid, COUNT(actor.id) as fcount FROM casts, actor WHERE casts.pid=actor.id AND actor.gender='F' GROUP BY casts.mid) F, (SELECT casts.mid, COUNT(actor.id) as mcount FROM casts, actor WHERE casts.pid=actor.id AND actor.gender='M' GROUP BY casts.mid) M WHERE movie.id=F.mid AND movie.id=M.mid) F ORDER BY F.ratio ASC, F.name;

--14--

SELECT R.name FROM (SELECT movie.name, CAST(SUM(ratings.rating) AS float)/COUNT(ratings.rating) as avg FROM movie, ratings WHERE movie.id=ratings.mid AND (cast(EXTRACT(YEAR FROM movie.year) as int)>=1990) AND (cast(EXTRACT(YEAR FROM movie.year) as int)<=2000) GROUP BY movie.name, movie.id ORDER BY avg DESC, movie.name LIMIT 10) R;

--15--

SELECT F.name FROM (SELECT M.name, Rat.avgRat FROM movie M, (SELECT R.mid ,AVG(R.rating) as avgRat FROM (SELECT userid FROM userProfile WHERE age BETWEEN 13 AND 21) U, ratings R WHERE U.userid=R.userid GROUP BY R.mid) Rat WHERE M.id = Rat.mid) F ORDER BY F.avgRat DESC, F.name;

--16--

select country from (select country,count(country) as freq from userProfile u,ratings r where u.userid=r.userid group by country order by freq desc,country limit 5) as foo;

--17--

SELECT ROUND(CAST(CAST(F.FC AS float)/M.MC AS numeric), 6) FROM (SELECT COUNT(*) AS FC FROM userProfile u, ratings r WHERE u.userid=r.userid AND u.gender='f') F, (SELECT COUNT(*) AS MC FROM userProfile u, ratings r WHERE u.userid=r.userid AND u.gender='m') M;

--18--

select userid,fname,lname from directors, (select did,userid,rank() over (partition by userid order by rating desc) as rank from (select did,userid,rating from ratings,moviedirectors where ratings.mid=moviedirectors.mid) as foo) as foo2 where rank=1 and directors.id=did order by userid;

--19--

select userid,did from (select userid,did,avg_rating,rank() over(partition by userid order by avg_rating desc) as dir_rank from (select userid,did,avg(rating) as avg_rating from (select did,userid,rating from ratings,moviedirectors where ratings.mid=moviedirectors.mid) as foo group by userid,did) as foo2) as foo3 where dir_rank=1 order by userid;

--20--

select genre,ROUND(avg_rating, 6),num_mv_rated, ROUND(CAST(CAST(num_mv_rated AS float) * 100  / (num_mv_rated + num_mv_not_rated) AS numeric),6) AS percentage from (select foo2.genre,foo2.avg_rating,foo2.num_mv_rated,foo1.num_mv_not_rated from (select bar.genre,count(bar.genre) as num_mv_not_rated from (select * from genre except (select genre.mid,genre.genre from genre,ratings where genre.mid=ratings.mid)) as bar group by bar.genre) as foo1, (select genre.genre, avg(rating) as avg_rating , count(rating) as num_mv_rated from genre,ratings where genre.mid=ratings.mid group by genre.genre) as foo2 where foo1.genre=foo2.genre) as foo3 order by avg_rating desc;

--21--

SELECT A.fname FROM (SELECT Act.fname, rank() over (ORDER BY Act.ActRat DESC) AS r FROM (SELECT a.fname, CAST(SUM(movRat5.AvgRating) AS float)/COUNT(AvgRating) AS ActRat FROM actor a, casts c,(SELECT m.name, m.id, CAST(SUM(indu.rating) AS float)/COUNT(indu.rating) AS AvgRating FROM movie m, (SELECT u.userid, r.mid, r.rating FROM userProfile u, ratings r WHERE u.userid=r.userid AND u.country='India') indu WHERE m.id=indu.mid GROUP BY m.name, m.id HAVING COUNT(indu.rating)>=5 ORDER BY AvgRating DESC) movRat5 WHERE a.id=c.pid AND c.mid=movRat5.id GROUP BY a.id, a.fname ORDER BY ActRat DESC, a.fname) Act) A WHERE A.r=1 Order BY A.fname;

--22--

SELECT DISTINCT U.userid FROM (SELECT ratings.userid, ratings.mid FROM ratings, (SELECT userid, MAX(rating) as max FROM ratings GROUP BY userid ORDER BY userid) M WHERE ratings.userid=M.userid AND ratings.rating=M.max) U, (SELECT ratings.mid FROM ratings, (SELECT MAX(rating) as max FROM ratings WHERE userid='user_000085' GROUP BY userid) X WHERE ratings.userid='user_000085' AND ratings.rating=X.max) E WHERE U.userid<>'user_000085' AND U.mid=E.mid ORDER BY U.userid;

--23--

SELECT M.year, SUM(R.avg)/COUNT(R.avg) as YearRat FROM (SELECT movie.id, cast(EXTRACT(YEAR FROM movie.year) as int) AS year FROM movie) M, (SELECT mid, CAST(SUM(rating) AS float)/COUNT(rating) as avg FROM ratings GROUP BY mid) R WHERE M.id=R.mid GROUP BY M.year ORDER BY YearRat DESC;

--24--

SELECT directors.fname, R.count FROM directors, (SELECT d.did, COUNT(M.mid) as count, rank() over (ORDER BY COUNT(M.mid) DESC) as r FROM (SELECT DISTINCT casts.mid FROM casts WHERE (casts.role='Himself' OR casts.role='Themselves')) M, movieDirectors d WHERE M.mid=d.mid GROUP BY d.did) R WHERE directors.id=R.did AND R.r=1;

--25--

select userid from (select userid,count(rating) as num_movies from ratings group by userid order by num_movies desc limit 10) as foo order by userid;

--26--

select country, movie_name from (select u.country as country, m.name as movie_name, avg(r.rating), rank() over (partition by u.country order by avg(r.rating) desc) as movie_rank from userProfile u, ratings r, movie m where u.userid = r.userid and r.mid = m.id group by u.country, m.id) as foo where movie_rank = 1;

--27--

select movie_name from (select movie_name, count(movie_name) as freq, rank() over (order by count(movie_name) desc) as freq_rank from (select movie_name from (select u.country as country, m.name as movie_name, avg(r.rating), rank() over (partition by u.country order by avg(r.rating) desc, m.name asc) as movie_rank from userProfile u, ratings r, movie m where u.userid = r.userid and r.mid = m.id group by u.country, m.id) as foo where movie_rank<=5) as temp_mv_names group by movie_name) as temp2 where freq_rank=1 ORDER BY movie_name asc;

--28--

select movie.name,freq from movie,(select mid, count(mid) as freq, rank() over (order by count(mid) desc) as freq_rank from (select userid, mid,rating, rank() over (partition by userid order by rating desc) as rank from ratings) as foo where rank<=5 group by mid) as temp2 where movie.id=temp2.mid and freq_rank<=10;

--29--

SELECT actor.fname, CAST(SUM(ratings.rating) as float)/COUNT(ratings.rating) as AvgRating FROM (SELECT casts.pid, rank() over (ORDER BY COUNT(movie.id) DESC) as r FROM casts, movie WHERE casts.mid=movie.id AND cast(EXTRACT(YEAR FROM movie.year) as int)<=1995 AND cast(EXTRACT(YEAR FROM movie.year) as int)>=1990 GROUP BY casts.pid ORDER BY r) R, casts, actor, ratings WHERE R.pid=casts.pid AND actor.id=R.pid AND ratings.mid=casts.mid AND R.r=1 GROUP BY actor.fname ORDER BY actor.fname;

--30--

select dir_fname,actor_fname from (select directors.fname as dir_fname,actor.fname as actor_fname,count((directors.id,actor.id)),rank() over (partition by directors.fname order by count((directors.id,actor.id)) desc) as rank from moviedirectors,casts,directors,actor where moviedirectors.did=directors.id and moviedirectors.mid=casts.mid and casts.pid=actor.id group by directors.id,actor.id) as foo where rank=1 order by dir_fname,actor_fname;
