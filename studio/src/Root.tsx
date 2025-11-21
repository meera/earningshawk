import React from 'react';
import {Composition, Folder} from 'remotion';
import {EarningsVideo} from './compositions/EarningsVideo';
import {EarningsCallVideo} from './compositions/EarningsVideoFull';
import {PLTR_Q3_2025} from './compositions/PLTR_Q3_2025';
import {PLTR_Q3_2025_take2} from './compositions/PLTR_Q3_2025-take2';
import {HOOD_Q3_2025} from './compositions/HOOD_Q3_2025';
import {BIP_Q3_2025} from './compositions/BIP_Q3_2025';
import {B_Q3_2025} from './compositions/B_Q3_2025';
import {PSKY_Q3_2025} from './compositions/PSKY_Q3_2025';
import {
	SubscribeExample,
	OutroExample,
	TitleExample,
	MetricsExample,
	FloatingMetricsExample,
	LogoExample,
	CompleteEndCardExample,
	FullDemo,
} from './compositions/Examples/AnimatedAssets';
import { SubscribeExample as SubscribeLowerThirdExample } from './compositions/Examples/SubscribeExample';
import { ThemeExample } from './compositions/ThemeExample';
import { EnhancementsDemo } from './compositions/EnhancementsDemo';
import { EarningsShort } from './compositions/EarningsShort';

/**
 * Root composition with three sections:
 *
 * 1. Production Videos - Actual earnings call videos
 * 2. YouTube Shorts - Vertical short-form videos (9:16)
 * 3. Animated Components - Individual component examples
 * 4. Component Library - Reusable components for building videos
 */
export const RemotionRoot: React.FC = () => {
	return (
		<>
			<Folder name="Production-Videos">
				<Folder name="Summary-Videos-50s">
					<EarningsVideo />
				</Folder>
				<Folder name="Full-Earnings-Calls">
					<EarningsCallVideo />
					<Composition
						id="HOOD-Q3-2025"
						component={HOOD_Q3_2025}
						durationInFrames={139254} // ~77 min at 30fps
						fps={30}
						width={1920}
						height={1080}
					/>
					<Composition
						id="PLTR-Q3-2025"
						component={PLTR_Q3_2025}
						durationInFrames={79000} // ~44 min at 30fps (adjust after insights)
						fps={30}
						width={1920}
						height={1080}
					/>
					<Composition
						id="PLTR-Q3-2025-take2"
						component={PLTR_Q3_2025_take2}
						durationInFrames={79000} // ~44 min at 30fps
						fps={30}
						width={1920}
						height={1080}
					/>
					<Composition
						id="BIP-Q3-2025"
						component={BIP_Q3_2025}
						durationInFrames={54826} // 30m 27s (1827.527s * 30fps)
						fps={30}
						width={1920}
						height={1080}
					/>
					<Composition
						id="B-Q3-2025"
						component={B_Q3_2025}
						durationInFrames={67904} // 37m 28s (2248.475s + 5s title + 10s CTA = 2263.475s * 30fps)
						fps={30}
						width={1920}
						height={1080}
					/>
					<Composition
						id="PSKY-Q3-2025"
						component={PSKY_Q3_2025}
						durationInFrames={79448} // 43m 53s (2633.268s + 5s title + 10s CTA = 2648.268s * 30fps)
						fps={30}
						width={1920}
						height={1080}
					/>
				</Folder>
			</Folder>

			<Folder name="YouTube-Shorts">
				<Composition
					id="EarningsShort"
					component={EarningsShort}
					durationInFrames={900} // 30 seconds at 30fps (adjust per short)
					fps={30}
					width={1080}  // 9:16 vertical format
					height={1920}
					defaultProps={{
						highlight: {
							text: "Revenue grew 24% driven by strong demand",
							speaker: "CEO",
							timestamp: 180,
							duration: 30,
							category: 'financial' as const,
						},
						audioUrl: 'http://192.168.1.101:8080/sample_audio.mp3',
						speakerPhotoUrl: 'http://192.168.1.101:8080/sample_photo.jpg',
						words: [
							{ word: 'Revenue', start: 0, end: 0.5 },
							{ word: 'grew', start: 0.6, end: 0.9 },
							{ word: '24%', start: 1.0, end: 1.4 },
							{ word: 'driven', start: 1.5, end: 1.9 },
							{ word: 'by', start: 2.0, end: 2.2 },
							{ word: 'strong', start: 2.3, end: 2.7 },
							{ word: 'demand', start: 2.8, end: 3.3 },
						],
						companyName: 'Sample Company',
						ticker: 'SMPL',
					}}
				/>
			</Folder>

			<Folder name="Animated-Components">
				<Composition
					id="ThemeExample"
					component={ThemeExample}
					durationInFrames={600}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="SubscribeLowerThirdExample"
					component={SubscribeLowerThirdExample}
					durationInFrames={500}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="SubscribeExample"
					component={SubscribeExample}
					durationInFrames={150}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="OutroExample"
					component={OutroExample}
					durationInFrames={240}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="TitleExample"
					component={TitleExample}
					durationInFrames={180}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="MetricsExample"
					component={MetricsExample}
					durationInFrames={150}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="FloatingMetricsExample"
					component={FloatingMetricsExample}
					durationInFrames={150}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="LogoExample"
					component={LogoExample}
					durationInFrames={180}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="CompleteEndCardExample"
					component={CompleteEndCardExample}
					durationInFrames={240}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="FullDemo"
					component={FullDemo}
					durationInFrames={360}
					fps={30}
					width={1920}
					height={1080}
				/>
				<Composition
					id="EnhancementsDemo"
					component={EnhancementsDemo}
					durationInFrames={1500}
					fps={30}
					width={1920}
					height={1080}
				/>
			</Folder>
		</>
	);
};
