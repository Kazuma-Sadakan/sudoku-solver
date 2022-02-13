from app import Sudoku
import pygame 

sudoku = Sudoku()

def main():
    sudoku.initialize()
    print("""
    start to solve -> s
    reset -> r
    quit -> q
    kill -> control c
    """)
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sudoku.reset()
                    sudoku.update()

                if event.key == pygame.K_s:
                    # sudoku.start()
                    sudoku.solve()
                    # sudoku.update()

                if event.key == pygame.K_q:
                    done = True
                    break

if __name__ == "__main__":
    main()