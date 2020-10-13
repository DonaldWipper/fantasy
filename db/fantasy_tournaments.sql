
create table fantasy_tournaments
(
    id bigint not null,
    name text not null,
    tag_id bigint not null,
    type text null,
    countries JSON null,
    priority bigint not null,
    flag JSON null,
    big_logo text null,
    created timestamp default CURRENT_TIMESTAMP not null,
    updated timestamp default CURRENT_TIMESTAMP not null,
    primary key (id)
);