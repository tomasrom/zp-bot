from parser import Parser, Parser_Zonaprops


def visto(link):
    return False


def no_vistos(links):
    return True


def main():

    return 0


# uncomment for test with the interactive shell ( python -i main.py ):

meliprops = Parser(
    website='https://inmuebles.mercadolibre.com.ar/departamentos/alquiler/capital-federal', # noqa
    soup_tag='a',
    next_page_path='/_Desde_',
    starts_with='https://departamento.mercadolibre.com.ar/MLA',
    page_limit=3,
    next_page_index=48,
)


argenprop = Parser(
    website='https://www.argenprop.com/departamento-alquiler-localidad-capital-federal', # noqa
    soup_tag='a',
    next_page_path='-pagina-',
    starts_with='/departamento-en-alquiler',
    page_limit=2,
    next_page_index=1,
)
