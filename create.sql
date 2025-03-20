CREATE TABLE public.calendrier (
    date_hour timestamptz,
    seasons varchar(60),
    holiday varchar(60),
    functioning_day varchar(10)
);


CREATE TABLE public.locations (
    date timestamptz
);

CREATE TABLE public.meteo_temp (
    date_str text,
    hour text,
    temperature text,
    humidity text,
    wind_speed text,
    visibility text,
    dew_point_temperature text,
    solar_radiation text,
    rainfall text,
    snowfall text
);
