from copy import deepcopy
from typing import List

from models.point import Point
from models.room import Room
from models.wall import Wall

import matplotlib.pyplot as plt
import math
import numpy as np

def generate_reflections(levels: int, starting_room: Room) -> List[Room]:
    all_reflections_list = []
    create_room_reflections(starting_room, all_reflections_list)

    previous_lvl_reflections = deepcopy(all_reflections_list)

    for i in range(levels - 1):
        current_lvl_reflections = []
        for current_room in previous_lvl_reflections:
            create_room_reflections(current_room, current_lvl_reflections)

        for reflection in current_lvl_reflections:
            if reflection not in all_reflections_list and not starting_room.equals(reflection):
                all_reflections_list.append(reflection)

        previous_lvl_reflections = current_lvl_reflections

    return all_reflections_list


def create_room_reflections(current_room: Room, reflections_list: List[Room]):
    left_reflection = deepcopy(current_room)
    left_reflection.move_room_left()
    switch_coefficient(left_reflection.left_wall, left_reflection.right_wall)

    left_reflection_transmitter_x = \
        left_reflection.left_wall.start_point.x + current_room.length - abs(left_reflection.transmitter.x - left_reflection.left_wall.start_point.x)
    left_reflection_transmitter_y = left_reflection.transmitter.y
    left_ref_transmitter = Point(left_reflection_transmitter_x, left_reflection_transmitter_y)
    left_reflection.transmitter = left_ref_transmitter


    top_reflection = deepcopy(current_room)
    top_reflection.move_room_up()
    switch_coefficient(top_reflection.top_wall, top_reflection.down_wall)

    top_ref_transmitter_x = top_reflection.transmitter.x
    top_ref_transmitter_y = \
        top_reflection.left_wall.start_point.y + current_room.height - abs(top_reflection.transmitter.y - top_reflection.left_wall.start_point.y)
    top_ref_transmitter = Point(top_ref_transmitter_x, top_ref_transmitter_y)
    top_reflection.transmitter = top_ref_transmitter


    right_reflection = deepcopy(current_room)
    right_reflection.move_room_right()
    switch_coefficient(right_reflection.left_wall, right_reflection.right_wall)

    right_reflection_transmitter_x = \
        right_reflection.left_wall.start_point.x + current_room.length - abs(right_reflection.transmitter.x - right_reflection.left_wall.start_point.x)
    right_reflection_transmitter_y = right_reflection.transmitter.y
    right_ref_transmitter = Point(right_reflection_transmitter_x, right_reflection_transmitter_y)
    right_reflection.transmitter = right_ref_transmitter


    down_reflection = deepcopy(current_room)
    down_reflection.move_room_down()
    switch_coefficient(down_reflection.top_wall, down_reflection.down_wall)

    down_ref_transmitter_x = down_reflection.transmitter.x
    down_ref_transmitter_y = \
        down_reflection.left_wall.start_point.y + current_room.height - abs(down_reflection.transmitter.y - down_reflection.left_wall.start_point.y)
    down_ref_transmitter = Point(down_ref_transmitter_x, down_ref_transmitter_y)
    down_reflection.transmitter = down_ref_transmitter

    if left_reflection not in reflections_list:
        reflections_list.append(left_reflection)

    if top_reflection not in reflections_list:
        reflections_list.append(top_reflection)

    if right_reflection not in reflections_list:
        reflections_list.append(right_reflection)

    if down_reflection not in reflections_list:
        reflections_list.append(down_reflection)


def switch_coefficient(first_wall: Wall, second_wall: Wall):
    temp = first_wall.coefficient
    first_wall.coefficient = second_wall.coefficient
    second_wall.coefficient = temp

# Given three colinear points p, q, r, the function checks if  
# point q lies on line segment 'pr'  
def onSegment(p, q, r): 
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y)) ): 
        return True
    return False
  
def orientation(p, q, r): 
    # to find the orientation of an ordered triplet (p,q,r) 
    # function returns the following values: 
    # 0 : Colinear points 
    # 1 : Clockwise points 
    # 2 : Counterclockwise 
      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y)) 
    if (val > 0): 
        # Clockwise orientation 
        return 1
    elif (val < 0): 
        # Counterclockwise orientation 
        return 2
    else: 
        # Colinear orientation 
        return 0
  
# The main function that returns true if  
# the line segment 'p1q1' and 'p2q2' intersect. 
def doIntersect(p1,q1,p2,q2): 
    # Find the 4 orientations required for  
    # the general and special cases 
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
  
    # General case 
    if ((o1 != o2) and (o3 != o4)): 
        return True
  
    # Special Cases 
  
    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
  
    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
  
    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
  
    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
  
    # If none of the cases 
    return False

def appendAlpha(already_added:List[Wall],new_wall:Wall):
    add=True
    for wall in already_added:
        if wall.start_point == new_wall.start_point or wall.start_point == new_wall.end_point:
            if wall.end_point == new_wall.start_point or wall.end_point == new_wall.end_point:
                add=False
        if wall.end_point == new_wall.start_point or wall.end_point == new_wall.end_point:
            if wall.start_point == new_wall.start_point or wall.start_point == new_wall.end_point:
                add=False
    return add

def cal_dist_from_srcs_to_rec(srcs_list:List[Room], rec_point:Point): #lista wszystkich odbitych pokoi , wsp. odbiornika
    dists_and_alfas_for_all = []
    for i in srcs_list:
        dist_and_alfas = []
        alfas = [0,0,0,0]
        ab = [rec_point.x - i.transmitter.x, rec_point.y - i.transmitter.y] #odcinek między źródłem a nadajnikiem
        d = math.sqrt(ab[0]**2+ab[1]**2)
        crossed_walls=[]
        for j in srcs_list:
            #sprawdzany ścianę górną
            if doIntersect(j.top_wall.start_point,j.top_wall.end_point,rec_point,i.transmitter):
                if appendAlpha(crossed_walls,j.top_wall):
                    crossed_walls.append(j.top_wall)
                    alfas[j.top_wall.coefficient] += 1
            #sprawdzamy scianę dolną
            if doIntersect(j.down_wall.start_point,j.down_wall.end_point,rec_point,i.transmitter):
                if appendAlpha(crossed_walls,j.down_wall):
                    crossed_walls.append(j.down_wall)
                    alfas[j.down_wall.coefficient] += 1
            #sprawdzamy ścianę lewą
            if doIntersect(j.left_wall.start_point,j.left_wall.end_point,rec_point,i.transmitter):
                if appendAlpha(crossed_walls,j.left_wall):
                    crossed_walls.append(j.left_wall)
                    alfas[j.left_wall.coefficient] += 1
            #sprawdzamy ścianę prawą
            if doIntersect(j.right_wall.start_point,j.right_wall.end_point,rec_point,i.transmitter):
                if appendAlpha(crossed_walls,j.right_wall):
                    crossed_walls.append(j.right_wall)
                    alfas[j.right_wall.coefficient] += 1
        dist_and_alfas=[d,alfas[0],alfas[1],alfas[2],alfas[3]] #tablica odległości i ilości przebicia przez ściany o wsp. alfax
        dists_and_alfas_for_all.append(dist_and_alfas)
    return dists_and_alfas_for_all

def cal_sum_intensity(spl, m, dists_and_alfas, coefs):
    Q = 20e-5*10**(spl/20)
    I = 0
    for i in dists_and_alfas:
        Itemp = Q/(4*math.pi*i[0]**2)*math.exp(-m*i[0])
        for j in range(3):
            Itemp *= (1-coefs[j])**i[j+1]
        I += Itemp
    return 10*math.log10(I/10**(-12))

def cal_echogram_and_plot(spl, m, dists_and_alfas, coefs):
    dists_and_alfas.sort(key=lambda d: d[0])
    c = 343 #speed of sound in normal conditions
    Q = 20e-5*10**(spl/20)
    dt_amps = np.array([0,0])
    for d in dists_and_alfas:
        amplitude = Q/(4*math.pi*d[0]**2)*math.exp(-m*d[0])
        for i in range(3):
            amplitude *= (1-coefs[i])**d[i+1]
        dt_amps = np.vstack((dt_amps,np.array([d[0]/c,amplitude])))
    dt, amps = dt_amps.T
    plt.figure()
    plt.stem(dt,amps,use_line_collection=True)
    plt.title("Room Impulse Response (Echogram)")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    return dt_amps

def schroeder_integral(dt_amps: np.ndarray):
    # zakładając, że jest impuls jest fizyczną deltą diraca
    # całka jest skokiem jednostkowym przeskalowanym o amplitudę
    # a energia całkowita jest sumą kwadratów amplitud
    dt, amps = dt_amps.T
    amps_dict = dict(zip(dt, amps))
    tot_energy = 0
    for a in amps:
        tot_energy += a**2

    schr_int = np.array([0,0])
    for i in range(len(dt)-1):
        inverse_int = 0
        for ti in reversed(dt):
            if ti >= dt[i]:
                inverse_int += amps_dict[ti]**2
        energy_decay = 10*math.log10(inverse_int/tot_energy)
        schr_int = np.vstack((schr_int,np.array([dt[i],energy_decay])))
    dt, energies = schr_int.T
    plt.figure()
    plt.step(dt,energies)
    plt.title('Schroeder energy decay curve')
    plt.xlabel('Time [s]')
    plt.ylabel('Energy decay magnitude [dB]')
    return schr_int

def linear_regression(x,y):
    m = (len(x) * np.sum(x*y) - np.sum(x) * np.sum(y)) / (len(x)*np.sum(x*x) - np.sum(x) ** 2)
    b = (np.sum(y) - m *np.sum(x)) / len(x)
    return [m,b]

def get_EDT_T20_T30_T60(schr_int: np.ndarray):
    dt, energies = schr_int.T
    list_params = []
    # EDT calc:
    if np.min(energies) <= -10:
        indexesEDT = np.where(energies>=-10) 
        EDT_energies = energies[indexesEDT]
        EDT_dt = dt[indexesEDT]
        linEDT = linear_regression(EDT_dt,EDT_energies)
        t0 = (0-linEDT[1])/linEDT[0]
        t1 = (-10-linEDT[1])/linEDT[0]
        edt = 6*(t1-t0)
        print("EDT =","%.3f" % edt, 's')
        list_params.append(edt)
    else:
        print('Cannot calc EDT!')
        list_params.append('-')
    # T20 calc:
    if np.min(energies) <= -25:
        indexesT20 = np.where(np.logical_and(energies<-5,energies>=-25))     
        t20_energies = energies[indexesT20]
        t20_dt = dt[indexesT20]
        lin20 = linear_regression(t20_dt,t20_energies)
        t0 = (-5-lin20[1])/lin20[0]
        t1 = (-25-lin20[1])/lin20[0]
        t20 = 3*(t1-t0)
        print("T20 =","%.3f" % t20, 's')
        list_params.append(t20)
    else:
        print('Cannot calc T20!')
        list_params.append('-')
    # T30 calc:
    if np.min(energies) <= -35:
        indexesT30 = np.where(np.logical_and(energies<-5, energies>-35))
        t30_energies = energies[indexesT30]
        t30_dt = dt[indexesT30]
        lin30 = linear_regression(t30_dt,t30_energies)
        t0 = (-5-lin20[1])/lin30[0]
        t1 = (-35-lin20[1])/lin30[0]
        t30 = 2*(t1-t0)
        print("T30 =","%.3f" % t30, 's')
        list_params.append(t30)
    else:
        print('Cannot calc T30!')
        list_params.append('-')
    # T60 calc:
    if np.min(energies) <= -65:
        indexesT60 = np.where(np.logical_and(energies<-5, energies>-65))
        t60_energies = energies[indexesT60]
        t60_dt = dt[indexesT60]
        lin60 = linear_regression(t60_dt,t60_energies)
        t0 = (-5-lin60[1])/lin60[0]
        t1 = (-65-lin60[1])/lin60[0]
        t60 = t1-t0
        print("T60 =","%.3f" % t60, 's')
        list_params.append(t60)
    else:
        print('Cannot cal T60!')
        list_params.append('-')
    return list_params

def get_C50_C80_D50_D80(dt_amps: np.ndarray, list_params: List):
    dt, amps = dt_amps.T
    # C50 calc:
    c50_early_energy = i = 0
    while dt[i] <= 0.05:
        c50_early_energy += amps[i]**2
        i += 1
    c50_late_energy = 0
    while i < len(dt):
        c50_late_energy += amps[i]**2
        i += 1
    c50 = 10*math.log10(c50_early_energy/c50_late_energy)
    print("C50 =","%.3f" % c50, 'dB')
    # C80 calc:
    c80_early_energy = i = 0
    while dt[i] <= 0.08:
        c80_early_energy += amps[i]**2
        i += 1
    c80_late_energy = 0
    while i < len(dt):
        c80_late_energy += amps[i]**2
        i += 1
    c80 = 10*math.log10(c80_early_energy/c80_late_energy)
    print("C80 =","%.3f" % c80, 'dB')
    # D50 calc:
    tot_energy = 0
    for a in amps:
        tot_energy += a**2
    d50_early_energy = i = 0
    while dt[i] <= 0.05:
        d50_early_energy += amps[i]**2
        i += 1
    d50 = 100*d50_early_energy/tot_energy
    print("D50 =","%.3f" % d50, '%')
    # D80 calc:
    d80_early_energy = i = 0
    while dt[i] <= 0.08:
        d80_early_energy += amps[i]**2
        i += 1
    d80 = 100*d80_early_energy/tot_energy
    print("D80 =","%.3f" % d80, '%')
    list_params.extend([c50, c80, d50, d80])
    return list_params