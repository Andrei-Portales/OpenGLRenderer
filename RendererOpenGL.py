import pygame
from pygame.locals import *
import numpy as np
from gl import Renderer, Model
import shaders
import glm


width = 960
height = 540

deltaTime = 0.0

pygame.init()
screen = pygame.display.set_mode(
    (width, height), pygame.DOUBLEBUF | pygame.OPENGL)
clock = pygame.time.Clock()

rend = Renderer(screen)

current_model = 0
models = [
    {'obj': 'model.obj', 'texture': 'model.bmp',
        'x': 0, 'y': 0, 'z': 2.66, 'radius': 5},
    {'obj': 'textures/wolf/WOLF.obj', 'texture': 'textures/wolf/WOLF.bmp',
        'x': 0, 'y': 0, 'z': 0, 'radius': 2, },
    {'obj': 'textures/eagle/eagle.obj', 'texture': 'textures/eagle/eagle.bmp',
        'x': 0, 'y': 0, 'z': 2.66, 'radius': 2},
    {'obj': 'textures/bear/bear.obj', 'texture': 'textures/bear/bear.bmp',
        'x': 0, 'y': 0, 'z': 2.66, 'radius': 5},
    {'obj': 'textures/mammoth/mammoth.obj', 'texture': 'textures/mammoth/mammoth.bmp',
        'x': 0, 'y': 0, 'z': 5, 'radius': 10},
]


def getModelWithConfig(index, rend):
    configs = models[index]
    model = Model(configs['obj'], configs['texture'])
    model.position.x = configs['x']
    model.position.y = configs['y']
    model.position.z = configs['z']
    rend.distanceRadius = configs['radius']
    return model


current_shader = 0
shaders = [
    {'vertex': shaders.vertex_shader,
        'fragment': shaders.fragment_shader, 'music': 'music/5.mp3'},
    {'vertex': shaders.vertex_toon_shader,
        'fragment': shaders.fragment_toon_shader, 'music': 'music/4.mp3'},
    {'vertex': shaders.vertex_rainbow_shader,
        'fragment': shaders.fragment_rainbow_shader, 'music': 'music/1.mp3'},
    {'vertex': shaders.vertex_static_shader,
        'fragment': shaders.fragment_static_shader, 'music': 'music/2.mp3'},
    {'vertex': shaders.vertex_toon_shader,
        'fragment': shaders.fragment_termic_shader, 'music': 'music/3.mp3'}
]


face = getModelWithConfig(current_model, rend)

shader = shaders[current_shader]
rend.setShaders(shader['vertex'], shader['fragment'])
pygame.mixer.music.load(shader['music'])
pygame.mixer.music.play(-1)

rend.scene.append(face)

rend.set_point_light(-10, 0, 0)

# play a song


isRunning = True
while isRunning:

    keys = pygame.key.get_pressed()

    # Traslacion de camara
    if keys[K_d]:
        target = rend.scene[0].position
        rend.rotateRight(target, 2)
    if keys[K_a]:
        target = rend.scene[0].position
        rend.rotateLeft(target, 2)

    if keys[K_w]:
        target = rend.scene[0].position
        rend.rotateUp(target, 2)
    if keys[K_s]:
        target = rend.scene[0].position
        rend.rotateDown(target, 2)

    # if keys[K_q]:
    #     rend.camPosition.y -= 1 * deltaTime
    # if keys[K_e]:
    #     rend.camPosition.y += 1 * deltaTime

    if keys[K_LEFT]:
        if rend.valor > 0:
            rend.valor -= 0.1 * deltaTime

    if keys[K_RIGHT]:
        if rend.valor < 0.2:
            rend.valor += 0.1 * deltaTime

    if keys[K_z]:
        #     rend.camRotation.y += 15 * deltaTime
        target = rend.scene[0].position
        rend.zoomIn(target, 2)
    if keys[K_x]:
        #     rend.camRotation.y -= 15 * deltaTime
        target = rend.scene[0].position
        rend.zoomOut(target, 2)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False

            if ev.key == K_1:
                rend.filledMode()
            if ev.key == K_2:
                rend.wireframeMode()
            if ev.key == K_3:
                current_shader -= 1
                shader = shaders[current_shader % len(shaders)]
                rend.setShaders(shader['vertex'], shader['fragment'])
                pygame.mixer.music.load(shader['music'])
                pygame.mixer.music.play(-1)
            if ev.key == K_4:
                current_shader += 1
                shader = shaders[current_shader % len(shaders)]
                rend.setShaders(shader['vertex'], shader['fragment'])
                pygame.mixer.music.load(shader['music'])
                pygame.mixer.music.play(-1)
            if ev.key == K_5:
                current_model -= 1
                rend.scene = [getModelWithConfig(
                    current_model % len(models), rend)]
            if ev.key == K_6:
                current_model += 1
                rend.scene = [getModelWithConfig(
                    current_model % len(models), rend)]

    if pygame.mouse.get_pressed()[0]:
        mouse_movement = pygame.mouse.get_rel()

        if mouse_movement[0] != 0:
            if mouse_movement[0] > 0:
                target = rend.scene[0].position
                rend.rotateRight(target, 3)
            elif mouse_movement[0] < 0:
                target = rend.scene[0].position
                rend.rotateLeft(target, 3)

        if mouse_movement[1] != 0:
            if mouse_movement[1] > 0:
                target = rend.scene[0].position
                rend.rotateUp(target, 3)
            elif mouse_movement[1] < 0:
                target = rend.scene[0].position
                rend.rotateDown(target, 3)

    rend.tiempo += deltaTime
    deltaTime = clock.tick(60) / 1000
    rend.render()
    pygame.display.flip()

pygame.quit()
