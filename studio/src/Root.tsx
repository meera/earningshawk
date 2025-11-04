import React from 'react';
import {Folder} from 'remotion';
import {EarningsVideo} from './compositions/EarningsVideo';
import {EarningsCallVideo} from './compositions/EarningsVideoFull';

/**
 * Root composition with two video types:
 *
 * 1. EarningsVideo (Summary) - 50-second highlight reel without audio
 * 2. EarningsCallVideo (Full) - 30-60 min full earnings call with audio overlays
 */
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Folder name="Summary Videos (50s)">
        <EarningsVideo />
      </Folder>
      <Folder name="Full Earnings Calls (30-60min)">
        <EarningsCallVideo />
      </Folder>
    </>
  );
};
