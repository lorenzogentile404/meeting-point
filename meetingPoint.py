import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import sys


# Support classes and funcionts
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, P):
        return self.x == P.x and self.y == P.y


def distance(P1, P2):
    return math.sqrt((P1.x - P2.x) ** 2 + (P1.y - P2.y) ** 2)


def area(P1, P2, P3):
    a = distance(P1, P2)
    b = distance(P2, P3)
    c = distance(P3, P1)
    s = (a + b + c) / 2
    s * (s - a) * (s - b) * (s - c)
    return math.sqrt(max(s * (s - a) * (s - b) * (s - c), 0))


def compute_barycenter(P1, P2, P3):
    return Point((P1.x + P2.x + P3.x) / 3, (P1.y + P2.y + P3.y) / 3)


def isPointInTriangle(P, A, B, C):
    area_ABC = area(A, B, C)
    area_PAB = area(P, A, B)
    area_PBC = area(P, B, C)
    area_PAC = area(P, A, C)
    return area_ABC == area_PAB + area_PBC + area_PAC


def isFair(M, A, B, C, cTollerance):
    percentageDetourA = percentageDetour(M, A, C)
    percentageDetourB = percentageDetour(M, B, C)
    # The second returned value is meaningful only when the first is True
    return abs(percentageDetourA - percentageDetourB) <= cTollerance, percentageDetourA


def objectiveFunction(M, A, B):
    return (distance(A, M) + distance(B, M)) / distance(M, C)


def percentageDetour(M, P, C):
    return (distance(P, M) + distance(M, C)) / distance(P, C)


# Input points
A = Point(0, 0)
B = Point(10, 3)
C = Point(6, 11)

xMin = min(A.x, B.x, C.x)
xMax = max(A.x, B.x, C.x)
yMin = min(A.y, B.y, C.y)
yMax = max(A.y, B.y, C.y)

# Plot the triangle
textShift = 1 / 2  # Adjust based on the plot
fig, ax = plt.subplots()
ax.scatter(A.x, A.y, color="red", s=100)
ax.text(A.x, A.y - textShift, "A", color="red", fontsize=12)
ax.scatter(B.x, B.y, color="red", s=100)
ax.text(B.x, B.y - textShift, "B", color="red", fontsize=12)
ax.scatter(C.x, C.y, color="red", s=100)
ax.text(C.x + textShift, C.y, "C", color="red", fontsize=12)
ax.plot([A.x, B.x], [A.y, B.y], "black")
ax.plot([B.x, C.x], [B.y, C.y], "black")
ax.plot([C.x, A.x], [C.y, A.y], "black")

# Plot the barycenter
G = compute_barycenter(A, B, C)
ax.scatter(G.x, G.y, color="blue", s=100)
ax.text(
    G.x,
    G.y - textShift,
    "G(" + str(round(G.x, 3)) + "," + str(round(G.y, 3)) + ")",
    fontsize=10,
    color="blue",
)
ax.text(
    G.x,
    G.y - textShift * 3 / 2,
    "f: "
    + str(round(objectiveFunction(G, A, B), 3))
    + " dA: "
    + str(round(percentageDetour(G, A, C), 3))
    + " dB: "
    + str(round(percentageDetour(G, B, C), 3)),
    fontsize=10,
    color="blue",
)


# Define the granularity of the search
xGranularity = (xMax - xMin) / 100
yGranularity = (yMax - yMin) / 100
cTollerance = min(xMax - xMin, yMax - yMin) / 1000
print(xGranularity, yGranularity, cTollerance)

fMin = sys.maxsize
fMax = 0
mCandidates = []
mOptimal = Point(0, 0)

# Search for the optimal meeting point
for x in np.arange(xMin, xMax, xGranularity):
    for y in np.arange(yMin, yMax, yGranularity):
        # Create candidate meeting point
        M = Point(x, y)
        # Exclude the vertices
        if not M.equals(A) and not M.equals(B) and not M.equals(C):
            # Compute the constraints
            cFairness, percentageDetourCandidate = isFair(M, A, B, C, cTollerance)
            cPointInTriangle = isPointInTriangle(M, A, B, C)
            if cFairness and cPointInTriangle:
                # Evalute objective function
                f = objectiveFunction(M, A, B)
                mCandidates.append((M, f, percentageDetourCandidate))
                if f < fMin:
                    fMin = f
                    mOptimal = M
                if f > fMax:
                    fMax = f

# Plot the candidate meeting points and the optimal point
for M, f, percentageDetourCandidate in mCandidates:
    # Compute the color based on the objective function value
    # The darker the color, the better (smaller) is the objective function value
    color = cm.viridis((f - fMin) / (fMax - fMin) if fMax != fMin else 1)
    size = 20
    if M.equals(mOptimal):
        size = 100
        ax.text(
            mOptimal.x + textShift,
            mOptimal.y,
            "M(" + str(round(mOptimal.x, 3)) + "," + str(round(mOptimal.y, 3)) + ")",
            fontsize=10,
            color=color,
        )
    ax.scatter(M.x, M.y, color=color, s=size)
    ax.text(
        M.x + textShift,
        M.y - textShift / 2,
        "f: " + str(round(f, 3)) + " d: " + str(round(percentageDetourCandidate, 3)),
        fontsize=10,
        color=color,
    )

# Set the aspect ratio to be equal
ax.set_aspect("equal")

# Add labels and title
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Optimal meeting point M")

# Display the plot
plt.grid(True)  # Add a grid for better readability
plt.show()
