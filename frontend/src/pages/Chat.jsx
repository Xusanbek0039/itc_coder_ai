import React, { useState, useEffect, useRef } from 'react';
import api from '../api/axios';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Image as ImageIcon, Plus, MessageSquare } from 'lucide-react';
import { cn } from '../lib/utils';

export default function Chat() {
    const [sessions, setSessions] = useState([]);
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [inputText, setInputText] = useState('');
    const [selectedImage, setSelectedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        fetchSessions();
    }, []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }

    const fetchSessions = async () => {
        try {
            const res = await api.get('chat/'); // Lists sessions
            setSessions(res.data);
            if (res.data.length > 0 && !currentSessionId) {
                loadSession(res.data[0].id);
            }
        } catch (err) {
            console.error("Failed to fetch sessions", err);
        }
    };

    const loadSession = async (id) => {
        setCurrentSessionId(id);
        try {
            const res = await api.get(`chat/${id}/`);
            setMessages(res.data.messages || []);
        } catch (err) {
            console.error("Failed to load session", err);
        }
    };

    const createNewSession = () => {
        setCurrentSessionId(null);
        setMessages([]);
    }

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputText.trim() && !selectedImage) return;

        const formData = new FormData();
        formData.append('message', inputText);
        if (selectedImage) {
            formData.append('image', selectedImage);
        }
        if (currentSessionId) {
            formData.append('session_id', currentSessionId);
        }

        // Optimistic Update
        const tempMsg = {
            id: Date.now(),
            sender: 'user',
            message: inputText,
            image: selectedImage ? URL.createObjectURL(selectedImage) : null,
            created_at: new Date().toISOString()
        };
        setMessages(prev => [...prev, tempMsg]);
        setInputText('');
        setSelectedImage(null);
        setLoading(true);

        try {
            const res = await api.post('chat/', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            const { session_id, user_message, bot_response } = res.data;

            if (!currentSessionId) {
                setCurrentSessionId(session_id);
                fetchSessions(); // Refresh list to show new session
            }

            // Replace temp message with real one and add bot response
            setMessages(prev => {
                const filtered = prev.filter(m => m.id !== tempMsg.id);
                return [...filtered, user_message, bot_response];
            });

        } catch (err) {
            console.error("Send failed", err);
        } finally {
            setLoading(false);
        }
    };

    const handleImageChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setSelectedImage(e.target.files[0]);
        }
    }

    return (
        <div className="flex h-[calc(100vh-100px)] gap-6">
            {/* Sidebar */}
            <div className="w-64 flex-shrink-0 bg-card border rounded-xl overflow-hidden flex flex-col hidden md:flex">
                <div className="p-4 border-b bg-muted/50">
                    <Button onClick={createNewSession} className="w-full flex items-center justify-center gap-2">
                        <Plus size={16} /> New Chat
                    </Button>
                </div>
                <div className="flex-1 overflow-y-auto p-2 space-y-2">
                    {sessions.map(session => (
                        <button
                            key={session.id}
                            onClick={() => loadSession(session.id)}
                            className={cn(
                                "w-full text-left p-3 rounded-lg text-sm transition-colors flex items-center gap-2",
                                currentSessionId === session.id
                                    ? "bg-primary/10 text-primary font-medium"
                                    : "hover:bg-muted"
                            )}
                        >
                            <MessageSquare size={14} />
                            <span className="truncate">Session {session.id}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Main Chat */}
            <div className="flex-1 flex flex-col bg-card border rounded-xl overflow-hidden shadow-sm">
                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                    <AnimatePresence>
                        {messages.length === 0 && !loading && (
                            <motion.div
                                initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                                className="h-full flex flex-col items-center justify-center text-muted-foreground p-8 text-center"
                            >
                                <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mb-4">
                                    <MessageSquare size={32} />
                                </div>
                                <h3 className="text-xl font-semibold text-foreground mb-2">Start a new conversation</h3>
                                <p>Ask me anything or upload an image to analyze!</p>
                            </motion.div>
                        )}
                        {messages.map((msg) => (
                            <motion.div
                                key={msg.id}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={cn("flex w-full", msg.sender === 'user' ? "justify-end" : "justify-start")}
                            >
                                <div className={cn(
                                    "max-w-[80%] rounded-2xl p-4 shadow-sm",
                                    msg.sender === 'user'
                                        ? "bg-primary text-primary-foreground rounded-br-sm"
                                        : "bg-muted text-foreground rounded-bl-sm"
                                )}>
                                    {msg.image && (
                                        <img
                                            src={msg.image.startsWith('blob:') ? msg.image : `http://127.0.0.1:8000${msg.image}`}
                                            alt="User upload"
                                            className="max-w-full rounded-lg mb-2 border border-black/10"
                                        />
                                    )}
                                    <p className="whitespace-pre-wrap leading-relaxed">{msg.message}</p>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    {loading && (
                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                            <div className="bg-muted px-4 py-3 rounded-2xl rounded-bl-sm flex items-center gap-2">
                                <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce [animation-delay:0.2s]" />
                                <div className="w-2 h-2 bg-foreground/30 rounded-full animate-bounce [animation-delay:0.4s]" />
                            </div>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-card border-t">
                    {selectedImage && (
                        <div className="mb-2 inline-flex items-center gap-2 bg-muted px-3 py-1 rounded-full text-xs">
                            <ImageIcon size={12} />
                            <span className="truncate max-w-[200px]">{selectedImage.name}</span>
                            <button onClick={() => setSelectedImage(null)} className="hover:text-destructive">×</button>
                        </div>
                    )}
                    <form onSubmit={handleSendMessage} className="flex gap-2">
                        <input
                            type="file"
                            id="file-upload"
                            accept="image/*"
                            className="hidden"
                            onChange={handleImageChange}
                        />
                        <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            onClick={() => document.getElementById('file-upload').click()}
                            className={selectedImage ? "text-primary bg-primary/10" : "text-muted-foreground"}
                        >
                            <ImageIcon size={20} />
                        </Button>
                        <Input
                            value={inputText}
                            onChange={(e) => setInputText(e.target.value)}
                            placeholder="Type your message..."
                            className="flex-1 rounded-full bg-muted/50 border-transparent focus:bg-background focus:border-input"
                        />
                        <Button type="submit" size="icon" className="rounded-full shadow-md" disabled={loading || (!inputText && !selectedImage)}>
                            <Send size={18} />
                        </Button>
                    </form>
                </div>
            </div>
        </div>
    );
}
