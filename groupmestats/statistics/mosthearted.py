import os

import jinja2
from PIL import Image as PILImage

from ..memberlookup import message_to_author
from ..statistic import statistic
from ..groupmeclient import get_groupme_client


class ScaledImage(object):
    def __init__(self, image_filename, max_height=200, max_width=200):
        self.link = image_filename
        pil_image = PILImage.open(image_filename)
        (self.width, self.height) = pil_image.size
        if self.height > max_height:
            self._resize(float(max_height) / self.height)
        if self.width > max_width:
            self._resize(float(max_width) / self.width)
        self.height = int(self.height)
        self.width = int(self.width)

    def _resize(self, scale):
        self.height *= scale
        self.width *= scale


@statistic
class MostHearted(object):
    def __init__(self, num_to_show=10):
        self._num_to_show = num_to_show

    def calculate(self, group, messages, **kwargs):
        client = get_groupme_client()
        heart_ordered = sorted(messages, reverse=True,
                               key=lambda message: len(message.favorited_by))
        num_to_show = min(self._num_to_show, len(messages))
        self._most_hearted = heart_ordered[0:num_to_show]
        for message in self._most_hearted:
            for i, attachment in enumerate(message.attachments):
                if attachment.type != "image":
                    continue
                filename = self._get_image_filename(message, i)
                if os.path.isfile(filename):
                    # Already downloaded, don't need to be slow and get it again
                    continue
                image_data = client.images.download(attachment)
                with open(filename, "wb") as f:
                    f.write(image_data)
        self._group_name = group.name

    def _get_image_filename(self, message, i):
        attachment = message.attachments[i]
        if ".png." in attachment.url:
            image_type = "png"
        elif ".jpeg." in attachment.url:
            image_type = "jpeg"
        elif ".gif." in attachment.url:
            image_type = "gif"
        else:
            raise RuntimeError("unknown format '%s'" % attachment.url)
        return "message-%s-%i.%s" % (message.id, i, image_type)

    def show(self):
        for message in self._most_hearted:
            message.author = message_to_author(message)
            message.images = []
            for i, attachment in enumerate(message.attachments):
                if attachment.type != "image": continue
                image_filename = self._get_image_filename(message, i)
                message.images.append(ScaledImage(image_filename))

        output_html_filename = "most_hearted_%s.html" % self._group_name
        with open(output_html_filename, "w", encoding='utf_16') as f:
            env = jinja2.Environment(loader=jinja2.PackageLoader("groupmestats"))
            # env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.getcwd()))
            template = env.get_template("template_most_hearted.html")
            html = template.render(messages=self._most_hearted, group=self._group_name)
            f.write(html)
        return output_html_filename
