"use client"

import { useAuth } from "@/store/useAuth";
import { ModeToggle } from "@/components/theme-toggle";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Home() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === 'ADMIN') router.push('/dashboard/admin');
      else if (user.role === 'TEACHER') router.push('/dashboard/teacher');
      else router.push('/dashboard/student');
    }
  }, [isAuthenticated, user, router]);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start text-center sm:text-left">
        <div className="flex items-center gap-4">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">
            IT Creative LMS AI
          </h1>
          <ModeToggle />
        </div>

        <p className="text-lg text-gray-600 dark:text-gray-300 max-w-lg">
          A next-generation AI-powered learning platform. Learn, Teach, and Grow with intelligent assistance.
        </p>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <Link
            href="/auth/register"
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            Get Started
          </Link>
          <Link
            href="/auth/login"
            className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
          >
            Login
          </Link>
        </div>
      </main>
    </div>
  );
}
