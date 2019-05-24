

#Example 15-4. Exrcising Lookingglass without a with block
from mirror import LookingGlass
manager = LookingGlass()

print(manager)


monster = manager.__enter__()
print(monster == 'JABBERWOCKY')

print(monster)

print(manager)

manager.__exit__(None, None, None)
print(monster)



"""
Results:
    <mirror.LookingGlass object at 0x7f83a6dfff98>
    eurT
    YKCOWREBBAJ 
    >89fffd6a38f7x0 ta tcejbo ssalGgnikooL.rorrim<
    JABBERWOCKY
"""