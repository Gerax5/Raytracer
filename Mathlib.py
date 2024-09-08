from math import pi, sin, cos, isclose


#Matriz por matriz, matriz por vector, normalizar un vector, magnitud de un vector, matriz de identidad, inversa de una matriz

def multiplyMatrixVector(matrix, vector):
    rows = len(matrix)
    cols= len(matrix[0])
    sizeVector = len(vector)
    
    if cols != sizeVector:
        raise ValueError("El número de columnas de la matriz debe ser igual al tamaño del vector.")

    result_vector = [0 for _ in range(rows)]

    for i in range(rows):
        for j in range(cols):
            result_vector[i] += matrix[i][j] * vector[j]
    
    return result_vector

def multiplyMatrixMatrix(matrix_a, matrix_b):
    rowsA, colsA = len(matrix_a), len(matrix_a[0])
    rowsB, colsB = len(matrix_b), len(matrix_b[0])
    
    if colsA != rowsB:
        raise ValueError("El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
    
    result = [[0 for _ in range(colsB)] for _ in range(rowsA)]
    
    for i in range(rowsA):
        for j in range(colsB):
            for k in range(colsA):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    
    return result

def normalizeVector(vector):
    magnitude = sum(x**2 for x in vector) ** 0.5
    if magnitude == 0:
        raise ValueError("No se puede normalizar un vector de magnitud cero.")
    return [x / magnitude for x in vector]

def magnitudeVector(vector):
    return sum(x**2 for x in vector) ** 0.5

def identityMatrix(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

def inverseMatrix(matrix):
    n = len(matrix)
    identity = identityMatrix(n)
    #Lo llame temp pero es una matriz aumentada
    temp = [row + identity[i] for i, row in enumerate(matrix)]

    for i in range(n):
        factor = temp[i][i]
        if factor == 0:
            raise ValueError("La matriz no es invertible.")
        for j in range(2 * n):
            temp[i][j] /= factor
        
        for k in range(n):
            if k != i:
                factor = temp[k][i]
                for j in range(2 * n):
                    temp[k][j] -= factor * temp[i][j]

    # Extraer la inversa de la matriz aumentada
    inverse = [row[n:] for row in temp]
    return inverse

def TranslationMatrix(x,y,z):
   return [ [1,0,0,x],
            [0,1,0,y],
            [0,0,1,z],
            [0,0,0,1]
         ]

def ScaleMatrix(x,y,z):
   return[  [x,0,0,0],
            [0,y,0,0],
            [0,0,z,0],
            [0,0,0,1]
         ]

def barycentricCoords(A, B, C, P):
	
	# Se saca el �rea de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1:
		return (u, v, w)
	else:
		return None
	


def RotationMatrixX(pitch, yaw, roll):
   #convertir a radianes
   pitch *= pi/180
   yaw *= pi/180
   roll *= pi/180
   
   #creamos la matriz de toracion para eje
   pitchMat = [[1,0,0,0],
               [0,cos(pitch),-sin(pitch),0],
               [0,sin(pitch),cos(pitch),0],
               [0,0,0,1]]

   yawMat = [  [cos(yaw),0,sin(yaw),0],
               [0,1,0,0],
               [-sin(yaw),0,cos(yaw),0],
               [0,0,0,1]
            ]

   rollMat = [ [cos(roll),-sin(roll),0,0],
               [sin(roll),cos(roll),0,0],
               [0,0,1,0],
               [0,0,0,1]
            ]
   
   #return pitchMat * yawMat * rollMat
   return multiplyMatrixMatrix(multiplyMatrixMatrix(pitchMat, yawMat), rollMat)


def dotProduct(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Los vectores deben tener la misma dimensión.")
    return sum(x * y for x, y in zip(vector1, vector2))

def crossProduct(vector1, vector2):
    if len(vector1) != 3 or len(vector2) != 3:
        raise ValueError("Ambos vectores deben ser de dimensión 3.")
    return [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]

def subtractVectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Los vectores deben tener la misma longitud")

    resultado = [v1[i] - v2[i] for i in range(len(v1))]
    
    return resultado

def multiplyVectorScalar(vector, scalar):
    result = [element * scalar for element in vector]
    return result

def sumVectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Both vectors must have the same length")

    
    result = [v1[i] + v2[i] for i in range(len(v1))]
    
    return result

def reflectVector(normal, direction):
    # R = 2 * (N * L)N - L
    reflect = 2 * dotProduct(normal, direction)
    reflect = multiplyVectorScalar(normal, reflect)
    reflect = subtractVectors(reflect, direction)
    reflect = normalizeVector(reflect)
    
    return reflect