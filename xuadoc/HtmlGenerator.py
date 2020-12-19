import re

from ReMatcher import ReMatcher

class HtmlGenerator:
    _BLOCK_MODE_CODE = "code"
    _BLOCK_MODE_COMMENT = "comment"

    _BLOCK_MODES = [
        _BLOCK_MODE_CODE,
        _BLOCK_MODE_COMMENT,
    ]

    _RENDER_MODE_PURE = "pure"
    _RENDER_MODE_DOC = "doc"
    _RENDER_MODE_NONE = "none"

    _RENDER_MODES = [
        _RENDER_MODE_PURE,
        _RENDER_MODE_DOC,
        _RENDER_MODE_NONE,
    ]

    _SYMBOL_NAME_RE_GROUP = r"([a-zA-Z_][a-zA-Z_0-9]*)"

    _PROPERTY_NAMES = {
        "xuadoc": [
            'renderComments',
            'renderCodes'
            ],
        "html": None,
    }

    _properties = {
        "xuadoc": {
            "renderComments": _RENDER_MODE_NONE,
            "renderCodes": _RENDER_MODE_DOC
        },
        "html": {},
    }

    _statements = []

    warnings = []

    _blocks = [
        {
            "mode": _BLOCK_MODE_CODE,
            "content": ""
        }
    ]

    def __init__(self, statements):
        self._statements = statements
        self._read()

    def _read(self):
        for statement in self._statements:
            m = ReMatcher(statement)
            
            ###############################
            # comment line
            if (m.match(r"\s*#\s*(.*)")):
                commentContent = m.group(1)
                m = ReMatcher(commentContent)

                # double comment
                if (m.match(r"--.*")):
                    # omit
                    continue

                # command
                elif (m.match(self._SYMBOL_NAME_RE_GROUP + r"\s*\.\s*" + self._SYMBOL_NAME_RE_GROUP + r"\s*=\s* (.*)")):
                    objectName = m.group(1)
                    propertyName = m.group(2)
                    value = m.group(3)
                    if (objectName not in self._PROPERTY_NAMES.keys()):
                        self.warnings.append("Unknown object " + objectName)
                        continue
                    if (self._PROPERTY_NAMES[objectName] is not None and propertyName not in self._PROPERTY_NAMES[objectName]):
                        self.warnings.append("Unknown property " + propertyName)
                        continue
                    self._properties[objectName][propertyName] = eval(value)

                # comment
                else:
                    if self._properties['xuadoc']['renderComments'] == self._RENDER_MODE_PURE:
                        self._appendCode(statement)
                    elif self._properties['xuadoc']['renderComments'] == self._RENDER_MODE_DOC:
                        m = ReMatcher(statement)
                        if (m.match(r"\s*#(    |\t)(.*)")):
                            self._appendCode(m.group(2))
                        else:
                            self._appendComment("\n" + commentContent)
                        continue
                    elif self._properties['xuadoc']['renderComments'] == self._RENDER_MODE_NONE:
                        # Do nothing
                        continue

            ###############################
            # code line
            else:
                if self._properties['xuadoc']['renderCodes'] == self._RENDER_MODE_PURE:
                    self._appendCode(statement)
                elif self._properties['xuadoc']['renderCodes'] == self._RENDER_MODE_DOC:
                    # TODO
                    continue
                elif self._properties['xuadoc']['renderCodes'] == self._RENDER_MODE_NONE:
                    # Do nothing
                    continue
    def render(self, template):
        doc = ""
        for block in self._blocks:
            if block["content"]:
                if block["mode"] == self._BLOCK_MODE_CODE:
                    doc += "<pre><code>" + block["content"] + "</code></pre>"
                else:
                    doc += "<div class = '" + block["mode"] + "'>" + self._html(block["content"]) + "</div>"

        result = template.replace("XUA-DOC-HOLDER", doc)

        result = re.sub(
            r'%\s*' + self._SYMBOL_NAME_RE_GROUP + '\s*(\?\?\s*(.*))?\s*%',
            lambda x : self._properties['html'][x[1]] if x[1] in self._properties['html'] else x[3],
            result
        )

        return result

    def _appendCode(self, statement):
        statement = statement.replace("\t", "    ")
        statement = statement.replace(" ", "&nbsp;")
        statement += "<br>" if statement.strip() != "" else ""
        if self._blocks[-1]["mode"] == self._BLOCK_MODE_CODE:
            self._blocks[-1]["content"] += statement
        if self._blocks[-1]["mode"] == self._BLOCK_MODE_COMMENT:
            self._blocks.append(
                {
                    "mode": self._BLOCK_MODE_CODE,
                    "content": statement
                }
            )

    def _appendComment(self, statement):
        if self._blocks[-1]["mode"] == self._BLOCK_MODE_COMMENT:
            self._blocks[-1]["content"] += statement
        if self._blocks[-1]["mode"] == self._BLOCK_MODE_CODE:
            self._blocks.append(
                {
                    "mode": self._BLOCK_MODE_COMMENT,
                    "content": statement
                }
            )

    def _html(self, statement):
        statement = statement.strip()

        # Bold
        statement = re.sub(
            r"\*\*(((?!\*\*).)*)\*\*",
            r"<strong>\1</strong>",
            statement
        )

        statement = re.sub(
            r"__(((?!__).)*)__",
            r"<strong>\1</strong>",
            statement
        )

        # Italic
        statement = re.sub(
            r"\*(((?!\*).)*)\*",
            r"<em>\1</em>",
            statement
        )
        
        statement = re.sub(
            r"_(((?!_).)*)_",
            r"<em>\1</em>",
            statement
        )

        # Inline Code
        statement = re.sub(
            r"`(((?!(?<!\\)`).)*)`",
            lambda x : "<code>" + x.group(1).replace(r"\`", "`") + "</code>",
            statement
        )

        # Image
        statement = re.sub(
            r"\!\[(((?!\]).)*)\]\s*\((((?!\)).)*)\)",
            r"<img alt='\1' src='\3'>",
            statement
        )

        # Link
        statement = re.sub(
            r"\[(((?!\]).)*)\]\s*\((((?!\)).)*)\)",
            r"<a href='\3'>\1</a>",
            statement
        )

        # h6
        statement = re.sub(
            r"^######(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h6 class='h6' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h6></a>",
            statement
        )

        # h5
        statement = re.sub(
            r"^#####(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h5 class='h5' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h5></a>",
            statement
        )

        # h4
        statement = re.sub(
            r"^####(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h4 class='h4' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h4></a>",
            statement
        )

        # h3
        statement = re.sub(
            r"^###(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h3 class='h3' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h3></a>",
            statement
        )

        # h2
        statement = re.sub(
            r"^##(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h2 class='h2' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h2></a>",
            statement
        )

        # h1
        statement = re.sub(
            r"^#(.*)",
            lambda x : "<a href='#" + x.group(1).strip().replace(' ', '_') + "'><h1 class='h1' id='" + x.group(1).strip().replace(' ', '_') + "'>" + x.group(1) + "</h1></a>",
            statement
        )

        # Unordered List
        # TODO

        # List
        # TODO

        return statement