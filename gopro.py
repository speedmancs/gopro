import argparse
import subprocess


def parse(input_file):
    videoFiles = []
    times = []
    with open(input_file, mode='r', encoding='utf-8') as file:
        for line in file.readlines():
            items = line.rstrip().split(',')
            if len(items) == 1:
                videoFiles.append(line.rstrip())
                times.append([])
            else:
                times[-1].append((items[0], items[1]))

    return videoFiles, times

if __name__ == "__main__":
    args = argparse.ArgumentParser(description='gopro tool')
    args.add_argument('-i', '--input', type=str, dest='input', help="input file")
    args.add_argument('-o', '--output', type=str, dest='output', help="output file")
    args = args.parse_args()
    videos, times = parse(args.input)
    count = len(videos)
    clip = 0
    for i in range(count):
        for t in times[i]:
            cutCmd = 'ffmpeg -i {} -ss {} -to {} -async 1 {}.mp4'.format(videos[i], t[0], t[1], clip + 1)
            clip = clip + 1
            subprocess.run(cutCmd, stdout=subprocess.PIPE)

    # merge the results
    file = open('list.txt', 'w')
    file.writelines(["file {}.mp4\n".format(i + 1) for i in range(clip)])
    file.close()
    concatCmd = 'ffmpeg -safe 0 -f concat -i list.txt -c copy {}'.format(args.output)
    subprocess.run(concatCmd, stdout=subprocess.PIPE)

    # reduce the size
    reduceCmd = 'ffmpeg -i {} -b 8507k smaller.mp4'.format(args.output)
    subprocess.run(reduceCmd, stdout=subprocess.PIPE)