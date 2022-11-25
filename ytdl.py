
import argparse
import os
import subprocess
from pytube import YouTube


def to_seconds(t: str):
	# t in hh:mm:ss format
	h, m, s = t.split(':')
	return 60*60*float(h) + 60*float(m) + float(s)


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('vid_link', type=str, help='link of YT vid')
	parser.add_argument('-ts', type=str, required=False, help='start time in hh:mm:ss:ms')
	parser.add_argument('-te', type=str,  required=False, help='end time in hh:mm:ss:ms')
	#parser.add_argument('-fp', type=str, required=False, help='file path (default is ytdl_downloads)')

	args = parser.parse_args()
	
	# only download progressive mp4 for now for simplicity
	# add option to download mp3 in the future
	
	yt_vid = YouTube(args.vid_link)
	streams = []
	dir_path = 'ytdl_downloads'
	
	print('Available streams:')
	for n, stream in enumerate(yt_vid.streams.filter(progressive=True)):
		print(f'{n} -- {stream}')
		streams.append(stream)
	
	stream_choice = int(input('Enter the stream # to download : '))
	stream = streams[stream_choice]
	
	print('Downloading stream...')
	stream.download(dir_path)
	print(f'Stream has finished downloading in "{dir_path}" !')

	title = yt_vid.title
	file_ext = stream.mime_type.split('/')[1]
	
	# swap out spaces and other junk in the title for _ to avoid problems
	junk = [' ']
	new_title = title
	for c in junk:
		new_title = new_title.replace(c, '_')
	
	old_filename = f'{dir_path}/{title}.{file_ext}'
	new_filename = f'{dir_path}/{new_title}.{file_ext}'
	os.rename(old_filename, new_filename)
	
	if args.ts and args.te:
		print('Trimming the video...')
		t1 = to_seconds(args.ts)
		t2 = to_seconds(args.te)
		# call ffmpeg from subprocess
		subprocess.run([
			'ffmpeg','-ss', str(t1),
			'-i', new_filename,
			'-t', str(t2 - t1),
			'-c', 'copy', f'{dir_path}/TRIMMED_{new_title}.{file_ext}'
		])
		os.remove(new_filename)
		print(f'Video has been trimmed into a clip from {args.ts} to {args.te} !')

# ffmpeg -ss [start] -i in.mp4 -t [duration] -c copy out.mp4


if __name__ == '__main__':
	main()


