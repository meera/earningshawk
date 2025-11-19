'use client';

import { PostHogIdentifier } from './PostHogIdentifier';

export function ClientLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <PostHogIdentifier />
      {children}
    </>
  );
}
