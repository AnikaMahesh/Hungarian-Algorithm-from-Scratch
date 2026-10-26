# Hungarian-Algorithm-from-Scratch
## Motivation
The hungarian algorithm is a optimization problem meant to solve assignment problems. An assignment problem is finding the optimal matching between 2 quantities minimizing a cost. Such as matching robots. to jobs that fit them minimizing the total amount of time robots spend working on tasks. This is normally a $O(n!)$ problem since it has to look though every permutation of robots doing tasks however the hungarian algorithm does it with $O(n^3)$ complexity.

## Use Cases
The Hungarian algorithm has many different applications such as in multi object tracking in videos -- matching objects detected in past frames to current ones based on distance or appearance similarity. It is also used in detection transformers to match predictions to ground truth. Additionally it can be used to assign people to classes or jobs or robots to jobs. 
## Explainer on how it works (with code)


## Discussion on when it works
This algorithm can only be applied to square matrices where it is possible to match each item from each of the 2 lists of quantities to each other. It cannot be used to match 1 item to 2 others for example. In addition to this it assumes the problem can be written in terms of a cost matrix and it cannot be easily than this algorithm will not help that much. However in square matrices where there is a optimal match between every item on the 2 lists it would work in all cases. 
