'use client';

import { useEffect } from 'react';
import { useSession } from '@/lib/auth-client';
import posthog from 'posthog-js';

/**
 * Hook to identify users in PostHog when they sign in
 * Handles both email/password and OAuth sign-ins
 */
export function usePostHogIdentify() {
  const { data: session } = useSession();

  useEffect(() => {
    if (session?.user) {
      const { email, name, id } = session.user;

      // Identify user in PostHog with email as the distinct ID
      if (email) {
        posthog.identify(email, {
          email,
          name: name || undefined,
          user_id: id,
        });
      }
    }
  }, [session]);
}
