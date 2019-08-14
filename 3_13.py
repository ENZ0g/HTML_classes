class Tag:
    def __init__(self, name='tag', is_single=False, output='', **attributes):
        self.name = name
        self.text = ''
        self.children = []
        self.is_child = False
        self.attributes = attributes
        self.is_single = is_single
        self.output = output

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.is_child:
            child_str = ''
            for i in self.children:
                child_str += str(i)
            if self.is_single:
                print(f'<{self.name}{self.pretty_attr()}>')
            else:
                print(f'<{self.name}{self.pretty_attr()}>{child_str}</{self.name}>')

    def __iadd__(self, other):
        self.children.append(other)
        other.is_child = True
        return self

    def __str__(self):
        if self.children:
            child_str = ''
            for i in self.children:
                child_str += str(i)
            return f'<{self.name}{self.pretty_attr()}>{self.text}{child_str}</{self.name}>'
        else:
            if self.is_single:
                return f'<{self.name}{self.pretty_attr()}>'
            else:
                return f'<{self.name}{self.pretty_attr()}>{self.text}</{self.name}>'

    def pretty_attr(self):
        if self.attributes:
            attr_list = ' '
            for attr, value in self.attributes.items():
                if attr =='klass':
                    attr = 'class'
                    temp_value = ''
                    for i in value:
                        temp_value += i + ' '
                    value = temp_value[0:-1]
                attr_list += f'{attr}="{value}" '
            return attr_list[0:-1]
        else:
            return ''


class TopLevelTag(Tag):
    pass

class HTML(Tag):
    def __enter__(self):
            return self

    def __exit__(self, *args):
        child_str = ''
        for i in self.children:
            child_str += str(i)
        if self.output:
            with open(self.output, 'w') as out_file:
                print(f'<html{self.pretty_attr()}>{child_str}</html>', file=out_file)
        else:
            print(f'<html{self.pretty_attr()}>{child_str}</html>')



with HTML(output='test.html') as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
        doc += head

    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text",)) as h1:
            h1.text = "Test"
            body += h1

        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
                div += img

            body += div

        doc += body
