def elimina_rep(match):

    for i in range(len(match)):

        for j in range(i+1,len(match)):
            if(j>=len(match)):
                break
            res_ori = match[i]
            res_con = match[j]

            # print(res_con["pagina"]," == ", res_ori["pagina"]," & ", res_con["salto"],"  == ", res_ori["salto"],"  & ", res_con["inicio"],"  == ", res_ori["inicio"])
            # print((int(res_con["pagina"]) == int(res_ori["pagina"])) & (int(res_con["salto"]) == int(res_ori["salto"])) & (int(res_con["inicio"]) == int(res_ori["inicio"])))

            if((int(res_con["pagina"]) == int(res_ori["pagina"])) & (int(res_con["salto"]) == int(res_ori["salto"])) & (int(res_con["inicio"]) == int(res_ori["inicio"]))):
                # print("Se elimino un elemento!")
                del match[j]
    return match
