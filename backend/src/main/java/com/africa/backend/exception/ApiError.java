package com.africa.backend.exception;

public record ApiError(
        int status,
        String message
) {
}
