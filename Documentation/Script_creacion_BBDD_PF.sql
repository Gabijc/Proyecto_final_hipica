CREATE TABLE disciplinas(
	id_disciplina SERIAL PRIMARY KEY,
	disciplina VARCHAR(50)
);
CREATE TABLE fechas(
	id_fecha SERIAL PRIMARY KEY,
	fecha DATE
);
CREATE TABLE caballos (
    id_caballo VARCHAR(50) PRIMARY KEY, -- Es la licencia del caballo
    nombre_caballo VARCHAR(50),
    sexo VARCHAR(50),
    edad INT,
    raza VARCHAR(50),
    nacionalidad VARCHAR(50),
    federacion VARCHAR(50),
    jinete_id INT REFERENCES ciudad(id_jinete) -- duda de si poner el ON DELETE CASCADE 
);
CREATE TABLE jinetes(
	id_jinete VARCHAR(50) PRIMARY KEY, 
    nombre_caballo VARCHAR(50),
    sexo VARCHAR(50),
    edad INT,
    raza VARCHAR(50),
    nacionalidad VARCHAR(50),
    federacion VARCHAR(50),
   disciplina_id INT REFERENCES disicplinas(id_disciplina)
);
CREATE TABLE resultados_completo(
	id_resultado SERIAL PRIMARY KEY,
    puesto INT,
    mer VARCHAR(50),
    puntos_doma INT,
    tiempo_obs_cross INT,
    tiempo_cross INT,
    ptos_obs_salto INT,
    ptos_tiempo_salto INT,
    ptos_total INT,
    estado VARCHAR(50),
    dinero_premio INT,
    disciplina_id INT REFERENCES disciplinas(id_disciplina) 	
);
CREATE TABLE resultados_salto(
	id_resultado SERIAL PRIMARY KEY,
    puesto INT,
    puntos_obs_r1 INT,
    tiempo_r1 INT,
    puntos_obs_r2 INT,
    tiempo_r2 INT,
    estado VARCHAR(50),
    dinero_premio INT,
    disciplina_id INT REFERENCES disciplinas(id_disciplina) 	
);
CREATE TABLE resultados_doma(
	id_resultado SERIAL PRIMARY KEY,
    puesto INT,
    nota_juez_E INT,
    nota_juez_H INT,
    nota_juez_C INT,
    nota_juez_B INT,
    nota_juez_M INT,
    nota INT,
    estado VARCHAR(50),
    dinero_premio INT,
    disciplina_id INT REFERENCES disciplinas(id_disciplina) 	
);
CREATE TABLE pruebas_completo(
    id_prueba SERIAL PRIMARY KEY,
    prueba VARCHAR(50),
    categoría VARCHAR (50),
    ámbito VARCHAR(50),
    id_fecha INT REFERENCES fechas(id_fecha),
    id_resultado INT REFERENCES resultados_completo(id_resultado)
);
CREATE TABLE pruebas_salto(
    id_prueba SERIAL PRIMARY KEY,
    prueba VARCHAR(50),
    categoría VARCHAR (50),
    altura_obstaculos INT,
    ámbito VARCHAR(50),
    id_fecha INT REFERENCES fechas(id_fecha),
    id_resultado INT REFERENCES resultados_salto(id_resultado)
);
CREATE TABLE pruebas_doma(
    id_prueba SERIAL PRIMARY KEY,
    prueba VARCHAR(50),
    categoría VARCHAR (50),
    ámbito VARCHAR(50),
    id_fecha INT REFERENCES fechas(id_fecha),
    id_resultado INT REFERENCES resultados_doma(id_resultado)
);
CREATE TABLE concursos(
    id_concurso SERIAL PRIMARY KEY,
    nombre VARCHAR(50),
    categoría VARCHAR(50),
    pais VARCHAR(50),
    provinicia VARCHAR(50),
    localidad VARCHAR(50),
    ámbito VARCHAR(50),
    federacion VARCHAR(50),
    id_fecha INT REFERENCES fechas(id_fecha)
);