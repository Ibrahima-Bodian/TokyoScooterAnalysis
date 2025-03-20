ALTER TABLE public.meteo_temp
  ALTER COLUMN temperature TYPE numeric USING (
    CASE 
      WHEN temperature ILIKE 'NA' THEN NULL 
      ELSE replace(temperature, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN humidity TYPE numeric USING (
    CASE 
      WHEN humidity ILIKE 'NA' THEN NULL 
      ELSE replace(humidity, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN wind_speed TYPE numeric USING (
    CASE 
      WHEN wind_speed ILIKE 'NA' THEN NULL 
      ELSE replace(wind_speed, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN visibility TYPE numeric USING (
    CASE 
      WHEN visibility ILIKE 'NA' THEN NULL 
      ELSE replace(visibility, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN dew_point_temperature TYPE numeric USING (
    CASE 
      WHEN dew_point_temperature ILIKE 'NA' THEN NULL 
      ELSE replace(dew_point_temperature, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN solar_radiation TYPE numeric USING (
    CASE 
      WHEN solar_radiation ILIKE 'NA' THEN NULL 
      ELSE replace(solar_radiation, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN rainfall TYPE numeric USING (
    CASE 
      WHEN rainfall ILIKE 'NA' THEN NULL 
      ELSE replace(rainfall, ',', '.')::numeric 
    END
  ),
  ALTER COLUMN snowfall TYPE numeric USING (
    CASE 
      WHEN snowfall ILIKE 'NA' THEN NULL 
      ELSE replace(snowfall, ',', '.')::numeric 
    END
  );
