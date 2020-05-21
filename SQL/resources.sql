create table resources
(
    resource_id     serial   not null constraint res_resources_pk primary key,
    res_type        text not null,
    res_class       text not null,
    res_subclass    text not null,
    res_title        text,
    res_path        text,
    file_name       text,
    reference_count integer,
    res_origin      text,
    imp_time        text,
    comment1        text,
    comment2        text,
    comment3        text,
    comment4        text,
    comment5        text
);

select * from resources where  res_type = 'video';
delete from resources where res_type = 'video';

drop table resources ;
truncate table resources;
select * from resources;

create table jobs
(
    job_id     serial   not null constraint job_id_pk primary key,
    job_name    text not null,
    job_status  text not null,
    contents    text not null,
    start_date  text,
    start_time  text,
    finish_date text,
    finish_time text,
    username    text,
    filename  text,
    thumbnail   text,
    comment     text
);

drop table jobs;
select * from jobs;

truncate  table jobs;

update jobs set job_status = '0' where job_id = 2;



create table Account
(
    user_id     serial   not null constraint user_id_pk primary key,
    name   text not null,
    password_hash    text not null,
    status      text not null,
    comment     text
);
select * from Account;