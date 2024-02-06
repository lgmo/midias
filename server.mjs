import Ffmpeg from "fluent-ffmpeg";

const silenceInfo = []

const silence = '-40dB'
const sildur = '1'
const file = 'video.mp4';
const results = Ffmpeg(file, { logger: console })
        .audioFilters([
            {
                filter: 'silencedetect',
                options: { n: silence, d: sildur }
            },
            {
                filter: 'silenceremove',
                options: { stop_threshold: silence, stop_periods: -1, stop_duration: sildur,  }
            }
        ])
        .on('codecData', function (data) {
            console.log('Input is ' + data.audio + ' audio ' + 'with ' + data.video + ' video');
        })
        .on('stderr', function (stderrLine) {
            if (stderrLine.includes(' silence_end: ')) {
                const endInfo = stderrLine.split(' silence_end: ')[1].split(' | silence_duration: ')
                const [endSec, duration] = endInfo.map(s => +s)
                silenceInfo.push({ stSec: endSec - duration, endSec, duration })
            }
        })
        .on('error', function (error) {
            console.error('Error:', error, silence);
        })
        .on('end', function () {
            console.log('Transcoding succeeded,  silenceInfo:', silenceInfo);
        })
        .save(`${file}-silenceRemoved.mp3`);
console.log(results);