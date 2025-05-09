CREATE TABLE disciplinas(
	id_disciplina SERIAL PRIMARY KEY,
	disciplina VARCHAR(50)
);
CREATE TABLE caballos(
    id_caballo VARCHAR(50) PRIMARY KEY, -- Es la licencia del caballo
    nombre VARCHAR(50),
    sexo VARCHAR(50),
    edad INT,
    raza VARCHAR(50),
    nacionalidad VARCHAR(50),
    federacion VARCHAR(50),
    id_resultado INT REFERENCES resultados(id_resultado) -- duda de si poner el ON DELETE CASCADE 
);
CREATE TABLE jinetes(
	id_jinete VARCHAR(50) PRIMARY KEY, 
    nombre VARCHAR(50),
    sexo VARCHAR(50),
    nacionalidad VARCHAR(50),
    federacion VARCHAR(50),
    id_resultado INT REFERENCES resultados(id_resultado) -- duda de si poner el ON DELETE CASCADE
);
CREATE TABLE pruebas(
    id_prueba SERIAL PRIMARY KEY,
    prueba VARCHAR(50),
    categoría VARCHAR (50),
    ámbito VARCHAR(50),
    fecha DATE
    id_disciplina INT REFERENCES disciplinas(id_disciplina)
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
);
CREATE TABLE resultados(
    id_resultado SERIAL PRIMARY KEY,
    puesto INT,
    estado VARCHAR(50),
    premio BOOLEAN, -- duda si tiene sentido, tipo true es que tiene premio y false que no tiene
    dinero_premio INT,
    id_jinete VARCHAR(50) REFERENCES jinetes(id_jinete)
    id_caballo VARCHAR(50) REFERENCES jinetes(id_caballo)
    id_prueba INT REFERENCES pruebas(id_prueba)
    id_concurso INT REFERENCES concursos(id_concurso)
)
CREATE TABLE resultados_doma(
	id_resultado INT REFERENCES resultados(id_resultado) -- duda de si poner el ON DELETE CASCADE
    id_prueba INT REFERENCES resultados(id_prueba) -- duda de si poner el ON DELETE CASCADE
    nota_juez_E INT,
    nota_juez_H INT,
    nota_juez_C INT,
    nota_juez_B INT,
    nota_juez_M INT,
    nota INT	
);
CREATE TABLE resultados_completo(
	id_resultado INT REFERENCES resultados(id_resultado) -- duda de si poner el ON DELETE CASCADE
    id_prueba INT REFERENCES resultados(id_prueba) -- duda de si poner el ON DELETE CASCADE
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