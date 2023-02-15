class ImageInContext:
    def __init__(self, image='', text='', title='', caption='', page_url=''):
        self.image = image
        self.text = text
        self.title = title
        self.caption = caption
        self.page_url = page_url

    def add_text(self, text):
        self.text += text.strip()
        if not self.text.strip().endswith('.'):
            self.text += '. '

    def add_title(self, text):
        self.title += text.strip()
        if not self.title.strip().endswith('.'):
            self.title += '. '

    def add_image(self, image):
        self.image = image

    def add_caption(self, text):
        self.caption += text.strip()
        if not self.caption.strip().endswith('.'):
            self.caption += '. '

    def get_constrained_text(self, limit=250):
        print('Constraining text to {} words'.format(limit))
        sentences = self.text.split('.')
        res = sentences.pop(0) + '.'
        while len(res.split()) < limit and len(sentences) > 0:
            res += sentences.pop(0)
            if len(sentences) > 0:
                res += '.'
        return res

    def __str__(self):
        return 'ImageInContext:\n  ' \
               'image: {}\n  ' \
               'caption: {}\n  ' \
               'title: {}\n  ' \
               'text: {}\n  ' \
               'page url: {}' \
            .format(self.image, self.caption, ' '.join(self.title.split()), '[' + str(len(self.text.split())) + ' words] ' + ' '.join(self.text.split()), self.page_url)

