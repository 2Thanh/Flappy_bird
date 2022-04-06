for event in pygame.event.get(): 
        if event.type== pygame.QUIT:
            run=False
        elif event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_SPACE and game_active:
                flap_sound.play()