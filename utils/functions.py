def urlnoticia(base, url):
    print("<------------------------------------------------>")

    # "sample_text": "El ministro de Relaciones Exteriores de Chile, Alberto van Klaveren, ya había expresado a inicios de mes su respaldo a la postura del gobierno peruano de asumir la presidencia pro tempore de la Alianza del Pacífico (AP). Ayer, el canciller del país sureño reiteró el aval de su país y se ofreció para lograr un acuerdo que venza la resistencia del mandatario mexicano Andrés Manuel López Obrador (AMLO) a entregarle el cargo a su homóloga peruana Dina Boluarte.",
	# "sample_link": "https://peru21.pe/politica/#:~:text=El%20ministro%20de,Boluarte.",  // url del texto del la noticia (%20 es un espacio)

    # https://peru21.pe/politica/chile-apoya-a-peru-ante-ataques-de-andres-manuel-lopez-obrador-y-gustavo-petro-noticia/#:~:text=“Hemos%20apoyado%20el,reconoció.
    resultado = base + url + ''
    
    return url
