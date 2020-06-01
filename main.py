from imgsrcs import *

if __name__ == '__main__':
    # PROGRAM INPUT
    # wymiary pomieszczenia: l x w, rząd metody źródeł pozornych
    l = 5
    w = 3
    order = 6
    # odległość nadajnika od lewego dolnego rogu (0,0) w metrach
    dist_src_from_left_wall = 3
    dist_src_from_down_wall = 2
    # odległość odbiornika od lewego dolnego rogu (0,0) w metrach
    dist_rec_from_left_wall = 0.5
    dist_rec_from_down_wall = 0.5
    # pogłowowe współczynniki pochłaniania w zakresie [0,1]
    alfa1 = 0.1 # lewa
    alfa2 = 0.2 # górna
    alfa3 = 0.5 # prawa
    alfa4 = 0.4 # dolna
    # parametry źródła wszechkierunkowego
    spl = 94 # poziom ciśnienia akustycznego na 1 m w dB, 
    m = 0.1 # mocowy współczynnik tłumienia m, zgodnie z PN ISO 9613-1
    # ------------------
    # CZĘŚĆ OBLICZENIOWA
    if (dist_src_from_left_wall <= l and dist_src_from_down_wall <= w \
        and dist_rec_from_left_wall <= l and dist_rec_from_down_wall <= w):
        p1 = Point(0, 0)    # lewy dolny
        p2 = Point(0, w)    # lewy górny
        p3 = Point(l, w)    # prawy górny
        p4 = Point(l, 0)    # prawy dolny

        rec_x = p1.x + dist_rec_from_left_wall
        rec_y = p1.y + dist_rec_from_down_wall
        rec_point = Point(rec_x,rec_y)
        coefs = [alfa1,alfa2,alfa3,alfa4]
        # założenia:
        # współrzędna "x" z "lewej" jest początkowa
        # współrzędna "y" z "dołu" jest początkowa
        # czyli z punktów (0, 0) i (l, 0) początkowym jest (0, 0) - x`owa z lewej
        # czyli z punktów (0, 0) i (0, w) początkowym jest (0, 0) - y`kowa z dołu
        
        w1 = Wall(deepcopy(p1), deepcopy(p2), 0)  # lewa
        w2 = Wall(deepcopy(p2), deepcopy(p3), 1)  # górna
        w3 = Wall(deepcopy(p4), deepcopy(p3), 2)  # prawa - celowa zamiana
        w4 = Wall(deepcopy(p1), deepcopy(p4), 3)  # dolna

        transmitter_x = p1.x + dist_src_from_left_wall
        transmitter_y = p1.y + dist_src_from_down_wall

        transmitter = Point(transmitter_x, transmitter_y)

        r = Room(w1, w2, w3, w4, transmitter)

        reflections = generate_reflections(order, r)

        all_walls = []
        for reflection in reflections:
            if reflection.left_wall not in all_walls:
                all_walls.append(reflection.left_wall)

            if reflection.top_wall not in all_walls:
                all_walls.append(reflection.top_wall)

            if reflection.right_wall not in all_walls:
                all_walls.append(reflection.right_wall)

            if reflection.down_wall not in all_walls:
                all_walls.append(reflection.down_wall)

        # sprawdzanie przebicia przez ściany o wsp. alfax
        dists_and_alfas = cal_dist_from_srcs_to_rec(reflections,rec_point)
        ab = [rec_x - transmitter_x, rec_y - transmitter_y] #odcinek między źródłem a nadajnikiem
        d = math.sqrt(ab[0]*ab[0]+ab[1]*ab[1])
        dists_and_alfas.append([d,0,0,0,0])

        # wizualizacja
        plt.figure()
        for wall in all_walls:
            if wall.coefficient==0:
                plt.plot([wall.start_point.x, wall.end_point.x], [wall.start_point.y, wall.end_point.y],'b')
            if wall.coefficient==1:
                plt.plot([wall.start_point.x, wall.end_point.x], [wall.start_point.y, wall.end_point.y],'g')
            if wall.coefficient==2:
                plt.plot([wall.start_point.x, wall.end_point.x], [wall.start_point.y, wall.end_point.y],'y')
            if wall.coefficient==3:
                plt.plot([wall.start_point.x, wall.end_point.x], [wall.start_point.y, wall.end_point.y],'r')

        for room in reflections:
            plt.plot([room.transmitter.x], [room.transmitter.y], 'bo')
        plt.plot(rec_point.x,rec_point.y,'ro')
        plt.plot([r.transmitter.x], [r.transmitter.y], 'bo')
        plt.title('Image-Sources Method view, blue - sources, red - receiver, order = %d' % order)
        plt.legend([r'$\alpha_R$=%.2f' % alfa3,r'$\alpha_U$=%.2f' % alfa2,r'$\alpha_L$=%.2f' % alfa1,r'$\alpha_D$=%.2f' % alfa4])
        plt.xlabel('X - Length [m]')
        plt.ylabel('Y - Width [m]')

        # główne obliczenia projektu i wykresy
        dt_amps = cal_echogram_and_plot(spl,m,dists_and_alfas,coefs)
        schr_int = schroeder_integral(dt_amps)
        acoustic_params = get_EDT_T20_T30_T60(schr_int)
        acoustic_params = get_C50_C80_D50_D80(dt_amps, acoustic_params)
        print("Summary intensity:","%.3f" % cal_sum_intensity(spl,m,dists_and_alfas,coefs),'dB')
        print("Number of virtual sources:",len(dists_and_alfas) - 1)
        print("Numer of walls:",len(all_walls))
        plt.show()
        # wizualizacja - koniec