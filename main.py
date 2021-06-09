from parser import Parser


def visto(link):
    return False


def no_vistos(links):
    return True


def main():
    argenprop = Parser(
            website='https://www.argenprop.com/departamento-alquiler-localidad-capital-federal', # noqa
            soup_tag='a',
            next_page='-pagina-',
            starts_with='/departamento-en-alquiler',
            page_limit=10,
            )
    no_vistos(argenprop.extract_links())
    # for testing :
    # links = argenprop.extract_links()
    # print(links)


main()


# uncomment for test with the interactive shell ( python -i main.py )
# argenprop = Parser(
#                website='https://www.argenprop.com/departamento-alquiler-localidad-capital-federal', # noqa
#                soup_tag='a',
#                next_page='-pagina-',
#                starts_with='/departamento-en-alquiler',
#                page_limit=2,
#            )
