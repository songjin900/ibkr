import pygame

def playMusic():
    try:
        # Initialize pygame
        pygame.init()

        # Load the WAV file
        pygame.mixer.music.load('purchaseMade.wav')

        # Play the loaded WAV file
        pygame.mixer.music.play()

        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)  # Adjust the tick rate as needed

        # Clean up
        pygame.quit()

    except:
        print("error in playMusic.py")
        pygame.quit()