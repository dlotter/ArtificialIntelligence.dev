from ComputerAI_3 import ComputerAI
from random import randint
import time

from BaseAI_3 import BaseAI

class PlayerAI(BaseAI):

    def getMove(self, grid):

        alfa = -999_999_999
        beta = +999_999_999
        prevTime = time.process_time()


        (child, _) = self.maximize(grid, alfa, beta, prevTime)

        return child

    def maximize(self, grid, alfa, beta, prevTime, limitador = 0):
        limitador += 1
        if self.terminalTest(grid, prevTime, limitador):
            return (None, self.calcUtility(grid))
        
        (maxChild, maxUtility) = (None, -999_999_999)

        for move in grid.getAvailableMoves():
            child = grid.clone()
            child.move(move)

            (_, utility) = self.minimize(child, alfa, beta, prevTime, limitador)

            if utility > maxUtility:
                (maxChild, maxUtility) = (move, utility)
            
            if maxUtility >= beta:
                break
            
            if maxUtility > alfa:
                alfa = maxUtility

        return (maxChild, maxUtility)

    def minimize(self, grid, alfa, beta, prevTime, limitador = 0):
            limitador +=1 
            if self.terminalTest(grid, prevTime, limitador):
                return (None, self.calcUtility(grid))
            
            (minChild, minUtility) = (None, 999_999_999)

            cells = grid.getAvailableCells()

            for move in cells:
                child = grid.clone()
                if move and child.canInsert(move):
                    child.setCellValue(move, 2)

                (_, utility) = self.maximize(child, alfa, beta, prevTime, limitador)

                if utility < minUtility:
                    (minChild, minUtility) = (move, utility)
                
                if minUtility <= alfa:
                    break
                
                if minUtility < beta:
                    beta = minUtility

            return (minChild, minUtility)


    def terminalTest(self, grid, prevTime, limitador):
        if time.process_time() - prevTime > 0.2 or limitador > 7:
            return True
        else:
            return False
    
    def calcUtility(self, grid):
        availableCellsHeuristic = len(grid.getAvailableCells())

        sortedCellsHeuristic = 0
        if sorted(grid.map[0], reverse=True) == grid.map[0]:
            sortedCellsHeuristic += 10
        if sorted(grid.map[1], reverse=True) == grid.map[1]:
            sortedCellsHeuristic += 10
        if sorted(grid.map[2], reverse=True) == grid.map[2]:
            sortedCellsHeuristic += 10

        maxTileHeuristic = 0
        if grid.map[-1][0] == grid.getMaxTile():
            maxTileHeuristic += 20

        adjacentHeuristic = 0
        for x in range(4):
            if grid.map[x][0] == grid.map[x][1]:
                adjacentHeuristic += 2
            if grid.map[x][1] == grid.map[x][2]:
                adjacentHeuristic += 2
            if grid.map[0][x] == grid.map[1][x]:
                adjacentHeuristic += 2
            if grid.map[1][x] == grid.map[2][x]:
                adjacentHeuristic += 2

        util = availableCellsHeuristic + sortedCellsHeuristic + maxTileHeuristic + adjacentHeuristic

        return util

