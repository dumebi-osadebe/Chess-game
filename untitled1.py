# importing required librarys
import pygame
import chess
import math

# Import the required module for text 
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
from playsound import playsound

#initialise display
X = 800
Y = 800
scrn = pygame.display.set_mode((X, Y))
pygame.init()

#basic colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

#initialise chess board
b = chess.Board()

#load piece images
pieces = {'p': pygame.image.load('./board_pieces/b_pawn.png').convert(),
          'n': pygame.image.load('./board_pieces/b_knight.png').convert(),
          'b': pygame.image.load('./board_pieces/b_bishop.png').convert(),
          'r': pygame.image.load('./board_pieces/b_rook.png').convert(),
          'q': pygame.image.load('./board_pieces/b_queen.png').convert(),
          'k': pygame.image.load('./board_pieces/b_king.png').convert(),
          'P': pygame.image.load('./board_pieces/w_pawn.png').convert(),
          'N': pygame.image.load('./board_pieces/w_knight.png').convert(),
          'B': pygame.image.load('./board_pieces/w_bishop.png').convert(),
          'R': pygame.image.load('./board_pieces/w_rook.png').convert(),
          'Q': pygame.image.load('./board_pieces/w_queen.png').convert(),
          'K': pygame.image.load('./board_pieces/w_king.png').convert(),
          
          }

# CONVERTING TEXT TO AUDIO
def text_to_speech(text):
    
    # Input: The text that you want to convert to audio
    
    mytext = text
    
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    audio = gTTS(text=mytext, lang=language, slow=False)
      
    # Saving the converted audio in a mp3 file named
    # welcome 
    audio.save("welcome.mp3")
      
    # Playing the converted file
    #os.system("start welcome.mp3")
    playsound("welcome.mp3")
    
def update(scrn,board):
    '''
    updates the screen basis the board class
    '''
    
    for i in range(64):
        piece = board.piece_at(i)
        if piece == None:
            pass
        else:
            scrn.blit(pieces[str(piece)],((i%8)*100,700-(i//8)*100))
    
    for i in range(7):
        i=i+1
        pygame.draw.line(scrn,WHITE,(0,i*100),(800,i*100))
        pygame.draw.line(scrn,WHITE,(i*100,0),(i*100,800))

    pygame.display.flip()
    
def main(BOARD):

    '''
    for human vs human game
    '''
    #make background black
    scrn.fill(BLACK)
    #name window
    pygame.display.set_caption('Chess')
    
    #variable to be used later
    index_moves = []

    status = True
    while (status):
        #update screen
        update(scrn,BOARD)

        for event in pygame.event.get():
     
            # if event object type is QUIT
            # then quitting the pygame
            # and program both.
            if event.type == pygame.QUIT:
                status = False

            # if mouse clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                #remove previous highlights
                scrn.fill(BLACK)
                #get position of mouse
                pos = pygame.mouse.get_pos()

                #find which square was clicked and index of it
                square = (math.floor(pos[0]/100),math.floor(pos[1]/100))
                index = (7-square[1])*8+(square[0])
                
                # ----------------------------------------------
                # CREATING AN ARRAY OF POSITIONS
                positions_num = []
                for i in range(8):
                    for j in range(8):
                        if j < 8:
                            positions_num.append(j)
                 # defining a range of characters           
                def char_range(c1, c2):
                    """Generates the characters from `c1` to `c2`, inclusive."""
                    for c in range(ord(c1), ord(c2)+1):
                        yield chr(c)
                        
                positions_alph = []
                for i in range(8):
                    for c in char_range('a', 'h'):
                        if c < 'i':
                            positions_alph.append(c)
                            
                text_to_speech("the position is " + positions_alph[index - 1] + str(positions_num[index] + 1))
                            
                if index not in index_moves:
                    #check the square that is clicked
                    piece = BOARD.piece_at(index)
                    #if empty pass
                    if piece == None:
                        
                        pass
                    else:
                        
                        #figure out what moves this piece can make
                        all_moves = list(BOARD.legal_moves)
                        
                        text_to_speech("You can move to the following positions ")
                                    
                        moves = []
                        for m in all_moves:
                            if m.from_square == index:
                                
                                moves.append(m)
                                
                                t = m.to_square
                                
                                TX1 = 100*(t%8)             #0,100,200...700 - left to right
                                TY1 = 100*(7-t//8)          #0,100,200...700 - top to bottom
    
                                #highlight squares it can move to
                                pygame.draw.rect(scrn,BLUE,pygame.Rect(TX1,TY1,100,100),5)
                                
                                text_to_speech(  positions_alph[int(TX1/100)] + str(positions_num[int(TY1/100)])  )
                        
                        index_moves = [a.to_square for a in moves]
                else:
                    move = None
                    move = moves[index_moves.index(index)]
                    print(move)
                    BOARD.push(move)

                    #reset index and moves
                    index=None
                    index_moves = []
                
     
    # deactivates the pygame library
        if BOARD.outcome() != None:
            print(BOARD.outcome())
            status = False
            print(BOARD)
    pygame.quit()
    

main(b)
















