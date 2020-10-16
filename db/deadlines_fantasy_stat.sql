--f
create table deadlines_fantasy_stat
(
    team_id bigint not null,
    team_name varchar(1000),
    team_link varchar(1000),
    tournament_id bigint not null,
    tournament_name varchar(1000),
    tournament_logo varchar(1000),
    deadline timestamp default CURRENT_TIMESTAMP not null,
    deadline_ts bigint not null,
    leagues_count  bigint default 0 not null,
    players_total bigint not null,
    place bigint not null,
    top bigint as (((`place` / `players_total`) * 100)) stored,
    points bigint not null,
    status tinyint default 0 not null,
    status_result text,
    color text null,
    from_players_ids text null,
    to_players_ids text null,
    updated timestamp default CURRENT_TIMESTAMP not null,
    is_actual tinyint(1) default 0 null,
    CONSTRAINT  `id_unique` PRIMARY KEY   (`deadline_ts`,`team_id`)
);