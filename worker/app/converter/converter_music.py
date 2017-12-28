from pydub import AudioSegment


class ConverterMusic:

    supported_formats = set(['m4a', 'mp3', 'flv', 'wav'])

    def can_convert(self, type_in, type_out):
        if type_in not in self.supported_formats:
            return False
        if type_out not in self.supported_formats:
            return False
        return True

    def convert(self, type_from, type_to, input, output):
        s = AudioSegment.from_file(input, type_from)
        s.export(output, format=type_to)

