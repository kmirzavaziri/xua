class config:
    data = {}

    @classmethod
    def init(cls):
        # @TODO sina implement
        cls.data['init'] = True
        return None

# clean

# call

def template(type, name, language = None):
    # @TODO sina implement
    return {}


def files(project, *, path = None, auto = None):
    # @TODO sina implement
    return []

class build:
    @staticmethod
    def general(project, source):
            # @TODO kamyar implement
        return 'file content'

    @staticmethod
    def server_php(source):
        # @TODO mehrdad implement
        # I think
        # return compiler.server_php_codegen(compiler.general_parse(compiler.general_lex(source)))
        # would be enough
        return 'php source code'

    @staticmethod
    def doc_html(source):
        # @TODO implement
        return ''

    @staticmethod
    def doc_latex(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_dart(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_javascript(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_typescript(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_java(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_kotlin(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_objectivec(source):
        # @TODO implement
        return ''

    @staticmethod
    def marshal_swift(source):
        # @TODO implement
        return ''

class compiler:
    @staticmethod
    def general_lex(source):
            # @TODO mehrdad implement
        return []

    @staticmethod
    def general_parse(tokens):
            # @TODO mehrdad implement
        return 'something idk'

    @staticmethod
    def server_php_codegen(ast):
            # @TODO mehrdad implement
        return 'php code'

