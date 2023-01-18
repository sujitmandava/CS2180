The following parts of the mentioned files were implemented:
1. search.py -> depthFirstSearch, breadthFirstSearch, uniformCostSearch, AStarSearch
2. SearchAgents.py -> CornersProblem(getStartState, isGoalState, getSuccessors), cornersHeuristic, foodHeuristic 

Execute the following commands to test the implemented code blocks:
python3 pacman.py
python3 pacman.py --layout testMaze --pacman GoWestAgent
python3 pacman.py --layout tinyMaze --pacman GoWestAgent
python3 pacman.py -h
python3 pacman.py -l tinyMaze -p SearchAgent -a fn=tinyMazeSearch
python3 pacman.py -l tinyMaze -p SearchAgent -a
python3 pacman.py -l tinyMaze -p SearchAgent
python3 pacman.py -l mediumMaze -p SearchAgent
python3 pacman.py -l bigMaze -z .5 -p SearchAgent
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python3 pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
python3 eightpuzzle.py
python3 pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python3 pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python3 pacman.py -l mediumScaryMaze -p StayWestSearchAgent
python3 pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic 
python3 pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python3 pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python3 pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
python3 pacman.py -l testSearch -p AStarFoodSearchAgent
python3 pacman.py -l trickySearch -p AStarFoodSearchAgent

Check Pacman AI Search: Report,pdf for details on the implementation and working of the search algorithms as well as heuristic design for the A* Search algortihm.