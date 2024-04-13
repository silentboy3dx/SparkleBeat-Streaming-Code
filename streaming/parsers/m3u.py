class M3U:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.parse()

    def create_record(self):
        return {
            'name': '',
            'artist': '',
            'file': '',
        }

    def parse(self):
        playlist = []
        with open(self.file_path, 'r', encoding='utf-8') as fp:
            lines: list = fp.readlines()
            if len(lines) == 0:
                return playlist

            entry = self.create_record()

            for index, line in enumerate(lines, 1):
                line = line.strip()

                if index == 1 and not line.startswith("#EXTM3U"):
                    raise ValueError(f"Invalid M3U File, missing #EXTM3U header")

                if not line:
                    continue

                if line.startswith("#EXTINF:"):
                    entry = self.create_record()
                    info = line.split(",")
                    if len(info) == 2:
                        info = info[1]
                        if '-' in info:
                            if info.count('-') > 1:
                                name, artist = info.split('-', 1)
                            else:
                                name, artist = info.split('-')
                            entry['name'] = name.strip()
                            entry['artist'] = artist.strip()

                elif not line.startswith('#'):
                    entry['file'] = line.strip()
                    playlist.append(entry)

        return playlist
