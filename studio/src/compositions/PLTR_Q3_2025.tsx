import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from 'remotion';

/**
 * PLTR Q3 2025 Earnings Video
 *
 * Data source: /var/earninglens/_downloads/jUnV3LiN0_k/
 * - source.trimmed.mp4 (audio)
 * - transcript.json (full transcript)
 * - insights.json (LLM analysis - when ready)
 */

// For now, using placeholder data
// Once insights.json is ready, import it dynamically
const PLTR_DATA = {
  company: 'Palantir Technologies',
  ticker: 'PLTR',
  quarter: 'Q3',
  fiscal_year: 2025,
  call_date: '2025-11-05',

  // TODO: Replace with actual data from insights.json
  financials: {
    revenue: {
      current: 0, // TODO: from insights
      previous: 0,
      yoy_growth: 0,
    },
    eps: {
      current: 0,
      estimate: 0,
      beat_miss: 'beat' as const,
    },
    segments: [
      {name: 'Government', revenue: 0},
      {name: 'Commercial', revenue: 0},
    ],
    margins: {
      gross: 0,
      operating: 0,
      net: 0,
    },
  },
  highlights: [
    'TODO: Extract from insights.json',
    'TODO: Key highlight 2',
    'TODO: Key highlight 3',
  ],
};

const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = interpolate(frame, [0, 30], [0.8, 1]);

  return (
    <AbsoluteFill className="bg-gradient-to-br from-indigo-900 via-gray-900 to-black flex items-center justify-center">
      <div
        style={{
          transform: `scale(${scale})`,
          opacity,
        }}
        className="text-center"
      >
        <h1 className="text-8xl font-bold text-white mb-6">
          {PLTR_DATA.company}
        </h1>
        <div className="text-6xl text-indigo-300 mb-8 font-mono">
          ${PLTR_DATA.ticker}
        </div>
        <h2 className="text-5xl text-gray-300">
          {PLTR_DATA.quarter} {PLTR_DATA.fiscal_year} Earnings Call
        </h2>
      </div>
    </AbsoluteFill>
  );
};

const SimpleBanner: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps, durationInFrames} = useVideoConfig();

  // Simple fade in at start
  const opacity = interpolate(frame, [0, 30], [0, 1], {extrapolateRight: 'clamp'});

  // Calculate elapsed time
  const totalSeconds = Math.floor(frame / fps);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  const timeDisplay = `${minutes}:${seconds.toString().padStart(2, '0')}`;

  return (
    <AbsoluteFill style={{opacity}}>
      {/* Top Banner */}
      <div className="absolute top-0 left-0 right-0 bg-gradient-to-b from-black/90 via-black/70 to-transparent p-6">
        <div className="flex items-center justify-between">
          {/* Left: Company Info */}
          <div>
            <div className="text-4xl font-bold text-white mb-1">
              {PLTR_DATA.company}
            </div>
            <div className="text-2xl text-indigo-300 font-mono">
              ${PLTR_DATA.ticker} · {PLTR_DATA.quarter} {PLTR_DATA.fiscal_year}
            </div>
          </div>

          {/* Right: Branding */}
          <div className="text-right">
            <div className="text-3xl font-bold text-white">EarningLens</div>
            <div className="text-lg text-gray-400">Earnings Call Analysis</div>
          </div>
        </div>
      </div>

      {/* Bottom Banner */}
      <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/90 via-black/70 to-transparent p-6">
        <div className="flex items-center justify-between">
          {/* Left: Call Info */}
          <div className="text-gray-300 text-xl">
            Earnings Call · {new Date(PLTR_DATA.call_date).toLocaleDateString('en-US', {
              month: 'long',
              day: 'numeric',
              year: 'numeric',
            })}
          </div>

          {/* Right: Time */}
          <div className="text-gray-400 text-xl font-mono">
            {timeDisplay}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const PLTR_Q3_2025: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();

  return (
    <AbsoluteFill className="bg-black">
      {/* Audio Track - Full earnings call (trimmed) */}
      {/* Symlinked from: /var/earninglens/_downloads/jUnV3LiN0_k/source.trimmed.mp4 */}
      <Audio src={staticFile('audio/PLTR_Q3_2025.mp4')} />

      {/* Title Card: 0-5s */}
      <Sequence from={0} durationInFrames={fps * 5}>
        <TitleCard />
      </Sequence>

      {/* Simple Banner Overlay - Full Duration (after title) */}
      <Sequence from={fps * 5} durationInFrames={durationInFrames - fps * 5}>
        <SimpleBanner />
      </Sequence>

      {/*
        MVP: Simple banner overlay only

        Future enhancements (after fixing context length):
        - Transcript subtitles
        - Key quotes from CEO/CFO
        - Revenue charts
        - EPS visualization
        - Guidance highlights
        - Q&A segments
      */}
    </AbsoluteFill>
  );
};
