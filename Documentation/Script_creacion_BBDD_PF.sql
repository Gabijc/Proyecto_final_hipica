CREATE TABLE disciplinas(
id_disciplina SERIAL PRIMARY KEY,
disciplina VARCHAR(50)
);

CREATE TABLE caballos(
id_caballo VARCHAR(50) PRIMARY KEY,
nombre_caballo VARCHAR(50)
);

CREATE TABLE jinetes(
id_jinete INT PRIMARY KEY,
nombre_jinete VARCHAR(50) 
);

CREATE TABLE concursos(
id_concurso SERIAL PRIMARY KEY,
nombre_concurso VARCHAR(255),
categoria_concurso VARCHAR(50),
pais_concurso VARCHAR(255),
provincia_concurso VARCHAR(255),
localidad_concurso VARCHAR(255),
ambito_concurso VARCHAR(50),
federacion_concurso VARCHAR(255),
fecha_inicio_concurso DATE,
fecha_fin_concurso DATE
);

CREATE TABLE pruebas(
id_prueba SERIAL PRIMARY KEY,
nombre_prueba VARCHAR(255),
fecha_prueba DATE,
id_disciplina INT REFERENCES disciplinas(id_disciplina)
);

CREATE TABLE resultados(
id_resultado INT PRIMARY KEY,
id_jinete INT REFERENCES jinetes(id_jinete),
id_caballo VARCHAR(50) REFERENCES caballos(id_caballo),
id_prueba INT REFERENCES pruebas(id_prueba),  
id_concurso INT REFERENCES concursos(id_concurso),
puesto INT,
estado VARCHAR(50),
premio BOOLEAN,
dinero_premio FLOAT
);

CREATE TABLE resultados_salto(
id_resultado INT PRIMARY KEY REFERENCES resultados(id_resultado), 
id_prueba INT REFERENCES pruebas(id_prueba), 
puntos_obs_r1 FLOAT,
puntos_tmp_r1 FLOAT,
tiempo_r1 FLOAT,
puntos_obs_r2 FLOAT,
puntos_tmp_r2 FLOAT,
tiempo_r2 FLOAT,
puntos_obs_r3 FLOAT,
puntos_tmp_r3 FLOAT,
tiempo_r3 FLOAT
);

CREATE TABLE resultados_doma(
id_resultado INT PRIMARY KEY REFERENCES resultados(id_resultado),  
id_prueba INT REFERENCES pruebas(id_prueba), 
nota_juez_E INT,
nota_juez_H INT,
nota_juez_C INT,
nota_juez_B INT,
nota_juez_M INT,
nota INT	
);

CREATE TABLE resultados_completo(
id_resultado INT PRIMARY KEY REFERENCES resultados(id_resultado),
id_prueba INT REFERENCES pruebas(id_prueba), 
mer VARCHAR(50),
puntos_doma FLOAT,
tiempo_obs_cross FLOAT,
tiempo_cross FLOAT,
ptos_obs_salto FLOAT,
ptos_tiempo_salto FLOAT,
ptos_total FLOAT	
);

